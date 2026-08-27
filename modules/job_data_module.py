"""
===================================================================
MODULE 4: JOB DATA MODULE - Job Descriptions Database
===================================================================
Role: Provide job descriptions for matching against resume.
Tech: Python built-in (curated database of real job roles)
===================================================================
"""


def get_job_database():
    """
    Returns a curated database of 15 real-world job roles
    with descriptions and required skills.
    
    Returns:
        list of dict: Each dict has title, category, description, required_skills
    """
    print("\n" + "=" * 60)
    print("  MODULE 4: JOB DATA - Loading Job Database")
    print("=" * 60)

    jobs = [
        {
            "title": "Python Developer",
            "category": "Software Engineering",
            "description": (
                "Develop and maintain Python applications. "
                "Write clean, efficient code using Python frameworks like Django and Flask. "
                "Work with REST APIs, databases including MySQL and PostgreSQL. "
                "Experience with git version control, unit testing, and agile methodologies. "
                "Knowledge of data structures, algorithms, and object-oriented programming."
            ),
            "required_skills": ["python", "django", "flask", "rest api", "mysql",
                                "git", "agile", "sql"]
        },
        {
            "title": "Data Scientist",
            "category": "Data Science",
            "description": (
                "Analyze large datasets using Python, pandas, and numpy. "
                "Build machine learning models using scikit-learn, tensorflow, and pytorch. "
                "Perform data visualization using matplotlib and tableau. "
                "Apply statistics, regression, classification, and clustering techniques. "
                "Experience with deep learning, neural networks, and NLP. "
                "Work with SQL databases and big data tools."
            ),
            "required_skills": ["python", "pandas", "numpy", "machine learning",
                                "tensorflow", "statistics", "sql", "data visualization",
                                "scikit-learn", "deep learning"]
        },
        {
            "title": "Frontend Developer",
            "category": "Web Development",
            "description": (
                "Build responsive web interfaces using React, Angular, or Vue. "
                "Strong proficiency in HTML5, CSS3, JavaScript, and TypeScript. "
                "Experience with webpack, REST APIs, and state management. "
                "Knowledge of UI/UX design principles, cross-browser compatibility. "
                "Familiarity with git, agile/scrum, and testing frameworks."
            ),
            "required_skills": ["javascript", "react", "html", "css", "typescript",
                                "rest api", "git", "agile"]
        },
        {
            "title": "Backend Developer",
            "category": "Software Engineering",
            "description": (
                "Design and implement server-side logic using Node.js, Python, or Java. "
                "Build RESTful APIs and microservices architecture. "
                "Work with databases like MongoDB, PostgreSQL, and Redis. "
                "Deploy using Docker, Kubernetes, and cloud platforms. "
                "Implement authentication, security, and performance optimization."
            ),
            "required_skills": ["python", "java", "node.js", "rest api", "mongodb",
                                "postgresql", "docker", "microservices"]
        },
        {
            "title": "Machine Learning Engineer",
            "category": "AI / ML",
            "description": (
                "Design and deploy machine learning models at scale. "
                "Work with tensorflow, pytorch, and scikit-learn. "
                "Build data pipelines using Python, pandas, and numpy. "
                "Experience with deep learning, computer vision, and NLP. "
                "Deploy models using Docker, AWS, and cloud infrastructure. "
                "Strong foundation in mathematics, statistics, and linear algebra."
            ),
            "required_skills": ["python", "machine learning", "tensorflow", "pytorch",
                                "deep learning", "docker", "aws", "numpy", "pandas"]
        },
        {
            "title": "DevOps Engineer",
            "category": "Cloud & DevOps",
            "description": (
                "Manage CI/CD pipelines using Jenkins, GitHub Actions. "
                "Container orchestration with Docker and Kubernetes. "
                "Infrastructure as code using Terraform and Ansible. "
                "Cloud platforms: AWS, Azure, or GCP. "
                "Linux system administration, monitoring, and logging. "
                "Scripting with Python, Bash, and shell scripting."
            ),
            "required_skills": ["docker", "kubernetes", "aws", "linux", "ci/cd",
                                "terraform", "jenkins", "python", "bash"]
        },
        {
            "title": "Full Stack Developer",
            "category": "Web Development",
            "description": (
                "Build end-to-end web applications. "
                "Frontend: React or Angular with HTML, CSS, JavaScript. "
                "Backend: Node.js or Django with REST APIs. "
                "Databases: MongoDB, PostgreSQL, MySQL. "
                "Version control with Git. Deployment with Docker. "
                "Agile/Scrum methodology and team collaboration."
            ),
            "required_skills": ["javascript", "react", "node.js", "python", "mongodb",
                                "html", "css", "git", "docker", "rest api"]
        },
        {
            "title": "Cloud Architect",
            "category": "Cloud & DevOps",
            "description": (
                "Design cloud-native solutions on AWS, Azure, or GCP. "
                "Architect microservices, serverless, and containerized applications. "
                "Implement security best practices and cost optimization. "
                "Experience with Kubernetes, Docker, and Terraform. "
                "Strong knowledge of networking, load balancing, and databases."
            ),
            "required_skills": ["aws", "azure", "gcp", "kubernetes", "docker",
                                "microservices", "serverless", "terraform"]
        },
        {
            "title": "Data Analyst",
            "category": "Data Science",
            "description": (
                "Analyze business data using SQL, Excel, and Python. "
                "Create dashboards and reports using Tableau or Power BI. "
                "Statistical analysis and data visualization with matplotlib. "
                "Clean and preprocess data using pandas and numpy. "
                "Present findings to stakeholders with clear communication."
            ),
            "required_skills": ["sql", "excel", "python", "tableau", "pandas",
                                "data visualization", "statistics", "communication"]
        },
        {
            "title": "Mobile App Developer",
            "category": "Mobile Development",
            "description": (
                "Develop mobile applications for iOS and Android. "
                "Languages: Swift, Kotlin, or React Native. "
                "REST API integration, local storage, and push notifications. "
                "UI/UX design implementation and performance optimization. "
                "App store deployment, testing, and maintenance."
            ),
            "required_skills": ["swift", "kotlin", "react", "javascript",
                                "rest api", "git"]
        },
        {
            "title": "Cybersecurity Analyst",
            "category": "Security",
            "description": (
                "Monitor and protect systems from security threats. "
                "Conduct vulnerability assessments and penetration testing. "
                "Implement firewalls, encryption, and access controls. "
                "Knowledge of Linux, networking, and security frameworks. "
                "Incident response, forensics, and compliance reporting."
            ),
            "required_skills": ["linux", "python", "networking", "sql",
                                "communication", "problem solving"]
        },
        {
            "title": "AI Research Scientist",
            "category": "AI / ML",
            "description": (
                "Conduct cutting-edge research in artificial intelligence. "
                "Publish papers on deep learning, reinforcement learning, and NLP. "
                "Implement novel architectures using PyTorch and TensorFlow. "
                "Strong mathematics: linear algebra, calculus, probability. "
                "Experience with computer vision, generative models, and transformers."
            ),
            "required_skills": ["python", "pytorch", "tensorflow", "deep learning",
                                "machine learning", "natural language processing",
                                "computer vision", "statistics"]
        },
        {
            "title": "Database Administrator",
            "category": "Database",
            "description": (
                "Manage and optimize database systems including MySQL, PostgreSQL, Oracle. "
                "Write complex SQL queries, stored procedures, and triggers. "
                "Database backup, recovery, and performance tuning. "
                "Data modeling, indexing, and replication strategies. "
                "Experience with NoSQL databases like MongoDB and Redis."
            ),
            "required_skills": ["mysql", "postgresql", "oracle", "sql", "mongodb",
                                "redis", "linux"]
        },
        {
            "title": "Project Manager (Tech)",
            "category": "Management",
            "description": (
                "Lead cross-functional technology teams using Agile and Scrum. "
                "Project planning, resource allocation, and risk management. "
                "Use tools like Jira, Confluence, and Slack for coordination. "
                "Strong leadership, communication, and presentation skills. "
                "Budget management, stakeholder reporting, and timeline tracking."
            ),
            "required_skills": ["project management", "agile", "scrum", "jira",
                                "leadership", "communication", "teamwork",
                                "presentation"]
        },
        {
            "title": "NLP Engineer",
            "category": "AI / ML",
            "description": (
                "Build natural language processing systems and text analytics. "
                "Work with NLTK, spaCy, and transformer models. "
                "Text classification, sentiment analysis, and named entity recognition. "
                "Experience with Python, deep learning, and neural networks. "
                "Deploy NLP models as APIs using Flask or FastAPI."
            ),
            "required_skills": ["python", "natural language processing", "machine learning",
                                "deep learning", "flask", "tensorflow"]
        },
    ]

    print(f"  > Loaded {len(jobs)} job roles from database")
    for job in jobs:
        print(f"    - {job['title']} ({job['category']})")

    return jobs
