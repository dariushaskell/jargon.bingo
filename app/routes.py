from flask import render_template, render_template_string, redirect, url_for, request, flash, session
from flask import current_app as app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User, Team, TeamMember, Friendship, ActiveSession, JargonItem, JargonList, Game, BingoCard
from app.email import send_verification_email, send_password_reset_email, send_invite_email
from app.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, InviteUserForm, CreateTeamForm, CompleteRegistrationForm, DeleteTeamForm, AddFriendForm, RemoveFriendForm, CreateGameForm
import random, string, uuid
from sqlalchemy.orm import aliased


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        username = form.username.data

        email_match = User.query.filter_by(email=email).first()
        if email_match:
            flash("Email already registered.", "error")
            return redirect(url_for("register"))
        
        username_match = User.query.filter_by(username=username).first()
        if username_match:
                flash("Username already taken.", "error")
                return redirect(url_for("register"))

        try:
            new_user = User(email=email)
            new_user.set_password(password)
            new_user.username = username
            db.session.add(new_user)
            db.session.flush()

            new_user.generate_verification_token()
            db.session.commit()

            send_verification_email(new_user)
            flash("Please check your email to verify your account.", "success")
        except Exception as e:
            db.session.rollback()
            flash("An error occurred during registration.", "error")
            print(str(e))
            return redirect(url_for("register"))

        return redirect(url_for("login"))
    return render_template("register.html", form=form, errors=form.errors)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash("Invalid email or password.", "error")
            return redirect(url_for("login"))

        login_user(user)
        session_id = str(uuid.uuid4())
        session['sid'] = session_id
        active_session = ActiveSession(user_id=user.id, session_id=session_id)
        db.session.add(active_session)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    if session.get('sid'):
        session_id = session.get('sid')
        active_session = ActiveSession.query.filter_by(session_id=session_id).first()
        if active_session:
            db.session.delete(active_session)
            db.session.commit()
    logout_user()
    return redirect(url_for("home"))

@app.route("/verify_email/<token>")
def verify_email(token):
    user = User.verify_email_token(token)
    if not user:
        flash("Invalid or expired token.")
        return redirect(url_for("login"))
    user.email_verified = True
    user.email_verification_token = None
    db.session.commit()
    flash("Your email has been verified. Please log in.", "success")
    return redirect(url_for("login"))

@app.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            user.generate_password_reset_token()
            send_password_reset_email(user)
        flash("Check your email for the instructions to reset your password.", "success")
        return redirect(url_for("login"))
    return render_template("reset_password_request.html", form=form)

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    print(token)
    user = User.verify_reset_token(token)
    if not user:
        flash("Invalid or expired token.")
        return redirect(url_for("reset_password_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        user.set_password(password)
        user.password_reset_token = None
        db.session.commit()
        flash("Your password has been reset.", "success")
        return redirect(url_for("login"))
    return render_template("reset_password.html", form=form, token=token)

@app.route("/resend_verification_token/<email>")
def resend_verification_token(email):
    user = User.query.filter_by(email=email).first()
    if user:
        if user.email_verified:
            flash("Your email is already verified.", "error")
        else:
            user.generate_verification_token()
            db.session.commit()
            send_verification_email(user)
            flash("Verification token has been resent. Please check your email.", "success")
    else:
        flash("User not found.", "error")
    return redirect(url_for("home"))

@app.route("/check_username", methods=["POST"])
def check_username():
    username = request.form.get("username")
    user = User.query.filter_by(username=username).first()
    if user:
        message = '<span id="username-check" class="taken">Username taken</span>'
    else:
        message = '<span id="username-check" class="available">Username available</span>'
    return render_template_string(message)

@app.route("/add_friend", methods=["POST"])
@login_required
def add_friend():
    form = AddFriendForm()
    if form.validate_on_submit():
        username = form.username.data
        friend = User.query.filter_by(username=username).first()
        if not friend:
            flash("User not found.", "error")
            return redirect(url_for("home"))

        existing_friendship = Friendship.query.filter_by(user_id=current_user.id, friend_id=friend.id).first()
        if existing_friendship:
            flash("You are already friends with this user.", "error")
            return redirect(url_for("home"))

        new_friendship = Friendship(user_id=current_user.id, friend_id=friend.id)
        db.session.add(new_friendship)
        db.session.commit()
        flash(f"{username} has been added to your friends.", "success")
    return redirect(url_for("home"))

@app.route("/delete_friend/<int:friend_id>", methods=["POST"])
@login_required
def delete_friend(friend_id):
    friendship = Friendship.query.filter_by(user_id=current_user.id, friend_id=friend_id).first()
    if friendship:
        db.session.delete(friendship)
        db.session.commit()
        flash("Friend removed successfully.", "success")
    else:
        flash("Friendship not found.", "error")
    return redirect(url_for("home"))

@app.route("/invite_user", methods=["POST"])
@login_required
def invite_friend():
    invite_form = InviteUserForm()
    create_team_form = CreateTeamForm()
    add_friend_form = AddFriendForm()
    remove_friend_form = RemoveFriendForm()

    if invite_form.validate_on_submit():
        email = invite_form.email.data
        password = random_password()
        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already registered.", "error")
            return redirect(url_for("home"))
        else:
            try:
                new_user = User(email=email)
                new_user.set_password(password)
                new_user.invited_by = current_user.id
                db.session.add(new_user)
                db.session.flush()
                new_user.generate_verification_token()

                new_friendship = Friendship(user_id=current_user.id, friend_id=new_user.id)
                db.session.add(new_friendship)

                db.session.commit()

                send_invite_email(new_user, inviter=current_user.email)
                flash(f"Your invitation has been successfully sent to {new_user.email}", "success")
                return redirect(url_for("home"))
            except Exception as e:
                db.session.rollback()
                flash("An error occurred during registration.", "error")
                print(str(e))
                return redirect(url_for("home"))

    return render_template(
        "home.html", 
        invite_form=invite_form, 
        create_team_form=create_team_form,
        add_friend_form=add_friend_form,
        remove_friend_form=remove_friend_form
    )

@app.route("/complete_registration/<token>", methods=["GET", "POST"])
def complete_registration(token):
    user = User.verify_email_token(token, inviter=True)
    if not user:
        flash("Invalid or expired token.")
        return redirect(url_for("login"))
    
    form = CompleteRegistrationForm()
    
    if form.validate_on_submit():
        username = form.username.data
        username_match = User.query.filter_by(username=username).first()
        if username_match:
            flash("Username already taken.", "error")
            return render_template('complete_registration.html', form=form, token=token)
        else:
            try:
                password = form.password.data
                user.set_password(password)
                user.username = username
                user.email_verified = True
                user.email_verification_token = None
                db.session.commit()
                login_user(user)
                flash("Your registration is complete.", "success")
                return redirect(url_for("home"))
            except Exception as e:
                db.session.rollback()
                flash("An error occurred during registration.", "error")
                print(str(e))
                return render_template('complete_registration.html', form=form, token=token)
    
    return render_template('complete_registration.html', form=form, token=token)

    
@app.route("/profile")
@login_required
def profile():
    active_sessions = ActiveSession.query.all()
    return render_template("profile.html", session=session, active_sessions=active_sessions)

@app.route("/card")
@login_required
def card():
    return render_template("card.html")

@app.route("/")
def home():
    if current_user.is_authenticated:
        friends = None
        teams = None
        friends = db.session.query(User).join(
            Friendship, 
            (Friendship.user_id == current_user.id) | (Friendship.friend_id == current_user.id)
        ).filter(
            (User.id != current_user.id) & 
            ((User.id == Friendship.user_id) | (User.id == Friendship.friend_id))
        ).all()

        teams = get_team_details(current_user.id)
        team_members_data = {team.team_id: get_team_members(team.team_id) for team in teams}

        teams_for_game_creation = get_teams_for_game_creation(current_user.id)
        jargon_lists_for_game_creation = get_jargon_lists_for_game_creation()

        invite_form = InviteUserForm()
        create_team_form = CreateTeamForm(friends=friends)
        delete_team_form = DeleteTeamForm()
        add_friend_form = AddFriendForm()
        remove_friend_form = RemoveFriendForm()
        create_game_form = CreateGameForm(teams=teams_for_game_creation, jargon_lists=jargon_lists_for_game_creation)


        print("Debug: Teams:", teams)
        print("Debug: Team members data:", team_members_data)

        return render_template(
            "home.html", 
            session=session, 
            invite_form=invite_form, 
            create_team_form=create_team_form,
            delete_team_form=delete_team_form, 
            friends=friends,
            teams=teams,
            team_members_data=team_members_data,
            add_friend_form=add_friend_form,
            remove_friend_form=remove_friend_form,
            create_game_form=create_game_form
        )
    return render_template("home.html")

@app.route("/delete_team/<int:team_id>", methods=["POST"])
@login_required
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
    if team.created_by != current_user.id:
        flash("You do not have permission to delete this team.", "error")
        return redirect(url_for("home"))

    try:
        TeamMember.query.filter_by(team_id=team.id).delete()
        db.session.delete(team)
        db.session.commit()
        flash(f"Team '{team.name}' deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the team.", "error")
        print(str(e))

    return redirect(url_for("home"))


@app.route("/create_team", methods=["POST"])
@login_required
def create_team():

    friends = db.session.query(User).join(
        Friendship, 
        (Friendship.user_id == current_user.id) | (Friendship.friend_id == current_user.id)
    ).filter(
        (User.id != current_user.id) & 
        ((User.id == Friendship.user_id) | (User.id == Friendship.friend_id))
    ).all()
    print(f"Debug: Friends: {friends}")

    form = CreateTeamForm(friends=friends)
    
    print("Debug: Form submitted:", request.form)
    print("Debug: Form data:", form.data)
    print("Debug: Available choices:", form.team_members.choices)

    if form.validate_on_submit():
        try:
            team_name = form.team_name.data
            team_members = form.team_members.data
            print(f"Debug: Creating team '{team_name}' with members: {team_members}")
            
            team = Team(name=team_name, created_by=current_user.id)
            db.session.add(team)
            db.session.flush()
            print(f"Debug: Team created with ID: {team.id}")
            
            for member in team_members:
                team_member = TeamMember(team_id=team.id, user_id=int(member))
                db.session.add(team_member)
                print(f"Debug: Added team member with user_id: {member}")
            
            db.session.commit()
            print("Debug: Changes committed to database")
            
            flash(f"Team {team_name} created successfully.", "success")
            return redirect(url_for("home"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while creating the team.", "error")
            print("Exception occurred:", str(e))
            return redirect(url_for("home"))
    else:
        print("Debug: Form validation failed")
        print("Debug: Form errors:", form.errors)
    return redirect(url_for("home"))


@app.route("/generate_card/<int:list_id>")
def generate_card(list_id):
    words = JargonItem.query.filter_by(list_id=list_id).all()
    random.shuffle(words)
    free_space = JargonItem(term="FREE")
    words.insert(12, free_space)
    return render_template("card.html", words=words[:25])

@app.route("/create_game", methods=["POST"])
@login_required
def create_game():
    form = CreateGameForm()  # Assuming a form for creating games
    if form.validate_on_submit():
        team_id = form.team_id.data
        list_id = form.list_id.data  # JargonList ID for generating cards
        online_members = ActiveSession.query.filter_by(team_id=team_id).all()
        
        # Create the game
        new_game = Game(
            hosted_by=current_user.id,
            team_id=team_id,
            jargon_list_id=list_id,
            start_time=datetime.utcnow(),
            status='ongoing'
        )
        db.session.add(new_game)
        db.session.flush()  # Get the game ID
        
        # Generate Bingo cards for online team members
        for member in online_members:
            bingo_card = generate_bingo_card(list_id)  # Implement this function based on your existing logic
            card_entry = BingoCard(
                game_id=new_game.id,
                user_id=member.user_id,
                card_data=bingo_card
            )
            db.session.add(card_entry)
        
        db.session.commit()
        
        # Redirect online members to the game screen
        for member in online_members:
            send_game_invite(member.user_id, new_game.id)  # Function to send a message/redirect
        
        flash("Game created and online members have been invited.", "success")
        return redirect(url_for("home"))
    
    flash("Failed to create the game. Check your inputs.", "error")
    return redirect(url_for("home"))

### Helper functions ###

def random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def get_team_details(user_id):
    query = db.session.query(
        Team.id.label('team_id'),
        Team.name.label('team_name'),
        (db.func.count(TeamMember.id) + 1).label('num_members'),
        db.case(
            (Team.created_by == user_id, True),
            else_=False
        ).label('is_owner')
    ).outerjoin(TeamMember, Team.id == TeamMember.team_id) \
     .filter(
         db.or_(
             TeamMember.user_id == user_id, 
             Team.created_by == user_id
         )
     ) \
     .group_by(Team.id)

    teams = query.all()

    return teams

def get_team_members(team_id):
    # Query to get team members excluding the owner
    members = db.session.query(
        User.username,
        User.email,
        TeamMember.joined_at
    ).join(TeamMember, User.id == TeamMember.user_id) \
     .filter(TeamMember.team_id == team_id) \
     .all()

    # Query to get the team owner
    owner = db.session.query(
        User.username,
        User.email,
        Team.created_at.label('joined_at')
    ).join(Team, User.id == Team.created_by) \
     .filter(Team.id == team_id) \
     .first()

    # Combine the owner and members into one list
    if owner:
        members.insert(0, owner)  # Add the owner at the beginning of the list

    return members

def get_teams_for_game_creation(user_id):
    # Query to get teams for game creation
    teams = Team.query.filter_by(created_by=user_id).all()
    return teams

def get_jargon_lists_for_game_creation():
    # Query to get jargon lists
    jargon_lists = JargonList.query.all()
    return jargon_lists



