import json

# JSON data
json_data = '''
{
  "categories": {
    "corporate": [
      "synergy", "leverage", "streamline", "value proposition", "pivot", "benchmark", "best practices",
      "core competency", "scalability", "alignment", "paradigm shift", "low-hanging fruit", "proactive",
      "touch base", "actionable insights", "ideation", "bandwidth", "quick wins", "holistic approach",
      "blue sky thinking", "disruptive", "thought leader", "stakeholder", "buy-in", "monetize", "brand equity",
      "customer-centric", "pain point", "mission-critical", "onboarding", "C-suite", "strategic fit", "deep dive",
      "optimization", "synergistic", "cross-functional", "empower", "knowledge transfer", "gap analysis", "win-win",
      "roadmap", "deliverables", "touchpoint", "ecosystem", "360-degree view", "customer journey",
      "value-added", "KPIs", "ROI", "benchmarking", "market penetration", "branding", "circle back", "pain points",
      "upskill", "results-driven", "moving the needle", "change management", "future-proof", "cloud-first",
      "best-of-breed", "bleeding edge", "value chain", "siloed", "bottom line", "out of the box", "dial it in",
      "low touch", "high touch", "pain-point", "quarterly earnings", "profit margins", "verticals", "horizontal integration",
      "margin"
    ],
    "software": [
      "API", "SDK", "agile", "scrum", "devops", "CI/CD", "microservices", "cloud-native", "containerization",
      "serverless", "frontend", "backend", "full stack", "REST", "SOAP", "GraphQL", "unit testing", "integration testing",
      "end-to-end testing", "TDD", "BDD", "version control", "git", "pull request", "merge conflict", "code review",
      "hotfix", "branching", "refactoring", "scalability", "load balancing", "caching", "latency", "API gateway",
      "proxy server", "middleware", "asynchronous", "synchronous", "event-driven", "state management", "ORM", "SQL",
      "NoSQL", "database schema", "migration", "rollback", "webhooks", "OAuth", "authentication", "authorization",
      "encryption", "hashing", "rate limiting", "sandbox", "debugging", "profiling", "optimization", "memory leak",
      "garbage collection", "threading", "concurrency", "race condition", "deadlock", "singleton", "MVC",
      "observer pattern", "factory pattern", "dependency injection", "CLI", "IDE", "syntax highlighting", "code linting",
      "compiler", "interpreter", "runtime environment"
    ],
    "hr": [
      "onboarding", "offboarding", "performance review", "360 feedback", "talent acquisition", "recruitment", "retention",
      "compensation", "benefits", "payroll", "employee engagement", "HRIS", "ATS", "job requisition", "succession planning",
      "learning and development", "upskilling", "reskilling", "employee relations", "compliance", "diversity and inclusion",
      "culture fit", "exit interview", "conflict resolution", "labor laws", "workplace safety", "EEO", "affirmative action",
      "job description", "job evaluation", "pay grade", "salary bands", "bonus structure", "talent pool", "candidate experience",
      "employee handbook", "FMLA", "PTO", "performance improvement plan", "disciplinary action", "grievance procedure",
      "employee recognition", "team building", "wellness programs", "HR analytics", "work-life balance", "remote work policy",
      "hybrid work model", "HRBP", "C&B", "employee turnover", "headcount", "organizational development", "HR metrics",
      "HR audit", "confidentiality agreement", "non-compete clause", "background check", "reference check", "recruitment funnel",
      "job offer", "job posting", "talent pipeline", "diversity hire", "job rotation", "employee satisfaction", "HR policies",
      "behavioral interview", "structured interview", "peer review", "skills assessment", "exit strategy", "workforce planning",
      "human capital", "job crafting"
    ],
    "engineering": [
      "CAD", "PLC", "SCADA", "Six Sigma", "lean manufacturing", "root cause analysis", "kaizen",
      "quality assurance", "quality control", "ISO standards", "prototype", "tolerance", "load testing", "stress testing",
      "material fatigue", "finite element analysis", "mechanical properties", "electrical schematics", "PCB design",
      "thermal analysis", "vibration analysis", "fluid dynamics", "CFD", "structural integrity", "ergonomics", "safety factor",
      "assembly line", "automation", "robotics", "nanotechnology", "renewable energy", "sustainability", "process optimization",
      "circuit design", "microcontroller", "embedded systems", "actuators", "sensors", "servo motor", "DC motor", "AC motor",
      "solenoid", "hydraulics", "pneumatics", "signal processing", "RFID", "IoT", "PLC programming", "control systems",
      "PID controller", "feedback loop", "data acquisition", "signal conditioning", "mechanical design", "CAD modeling", "3D printing",
      "additive manufacturing", "subtractive manufacturing", "composites", "alloys", "thermoplastics", "elastomers", "biomaterials",
      "nanomaterials", "optoelectronics", "photonics", "mechatronics", "geotechnical", "structural analysis", "civil engineering",
      "environmental engineering", "energy efficiency", "thermal conductivity", "vibration isolation", "shock absorption"
    ],
    "buzzwords": [
      "disruptive", "innovative", "pivot", "unicorn", "hypergrowth", "blockchain", "big data", "AI", "machine learning",
      "deep learning", "5G", "IoT", "AR", "VR", "NFT", "metaverse", "cryptocurrency", "bitcoin", "ethereum", "cloud computing",
      "SaaS", "PaaS", "IaaS", "edge computing", "quantum computing", "smart contract", "decentralization", "fintech", "proptech",
      "insurtech", "edtech", "healthtech", "biotech", "green tech", "agritech", "adtech", "gig economy", "sharing economy",
      "circular economy", "carbon footprint", "net zero", "sustainability", "ESG", "impact investing", "brand activism", "micro-moments",
      "customer experience", "omnichannel", "personalization", "user-centric", "growth hacking", "viral marketing", "storytelling",
      "brand loyalty", "influencer marketing", "social proof", "fomo", "gamification", "community building", "crowdsourcing",
      "design thinking", "lean startup", "agile transformation", "digital transformation", "future of work", "remote-first",
      "hybrid work", "digital nomad", "gig worker", "side hustle", "subscription model", "freemium", "monetization", "data-driven",
      "real-time analytics"
    ]
  }
}
'''

# Load JSON data
data = json.loads(json_data)

# Function to verify the number of words in each category
def verify_word_counts(data):
    categories = data["categories"]
    for category, words in categories.items():
        print(f"Category: {category}, Number of Words: {len(words)}")

# Verify word counts
verify_word_counts(data)
