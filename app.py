"""
Flow Remote Ops -- Flask app.

Pages:
  /                          landing page
  /contact                   "Build Your Remote Team" lead form
  /vision-and-mission        Vision & Mission page
  /faq                       dedicated FAQ page
  /blog                      Blog landing page (no posts yet)
  /services/<slug>           one dedicated page per service category
  /who-we-help/<slug>        one dedicated page per audience type
  /talents/<slug>            one placeholder page per Talents nav link

There is no backend form handler yet -- the lead form on /contact is a
real set of fields, but submitting it doesn't send anywhere until you
connect it to a destination (Google Forms or your own endpoint). See
submitLeadForm() in static/js/script.js for where to wire that up.

Run locally:
    pip install -r requirements.txt
    python app.py
Then visit http://localhost:5000
"""

from flask import Flask, render_template, abort

app = Flask(__name__)

# ----------------------------------------------------------------------
# Service category pages (Employers dropdown > Services column)
# ----------------------------------------------------------------------
SERVICE_PAGES = {
    "sales-business-development": {
        "title": "Sales & Business Development",
        "tagline": "Keep your pipeline moving without hiring an in-house team.",
        "description": "A remote specialist handling lead generation, prospect research, and outreach so your sales pipeline keeps moving even when your team is stretched thin. Rather than losing potential clients to slow follow-up, you get someone dedicated to keeping conversations moving and appointments booked, without the cost and ramp-up time of a full-time hire.",
        "included": ["Lead Generation", "Prospect Research", "Client Outreach", "Appointment Setting", "Sales Support"],
    },
    "operations-administration": {
        "title": "Operations & Administration",
        "tagline": "Keep the day-to-day running smoothly.",
        "description": "Reliable support for the administrative and operational work that keeps a business functioning — from managing your CRM to handling customer inquiries and keeping projects on track. This is often the first area where things start to slip as a business grows; a dedicated remote specialist keeps that from happening.",
        "included": ["Administrative Support", "CRM Management", "Customer Support", "Project Management", "Bookkeeping"],
    },
    "marketing-creative": {
        "title": "Marketing & Creative",
        "tagline": "Consistent content and outreach, without the agency retainer.",
        "description": "A remote specialist to keep your marketing consistent — managing social channels, producing graphics and video, and handling outreach — matched to what your business actually needs. This works well for businesses that know marketing matters but don't have the bandwidth to keep it running every week.",
        "included": ["Social Media Management", "Graphic Design", "Video Editing", "SEO / Backlink Outreach"],
    },
    "technology-automation": {
        "title": "Technology & Automation",
        "tagline": "Technical support without a full-time hire.",
        "description": "Remote support for web development and automation work, so your site and internal systems keep improving without needing a full-time technical hire. This can range from small website updates to setting up automations that remove repetitive manual work from your team's plate.",
        "included": ["Web Development", "AI Automation", "CRM Automation"],
    },
}

# ----------------------------------------------------------------------
# Audience pages (Employers dropdown > Who We Help column)
# ----------------------------------------------------------------------
WHO_WE_HELP_PAGES = {
    "growing-businesses": {
        "title": "Growing Businesses",
        "tagline": "Add capacity without adding overhead.",
        "description": "When the workload grows faster than the team, it's easy to end up firefighting instead of building. A remote specialist can pick up the operational or sales work that's piling up, in weeks rather than the months a full hiring process usually takes.",
        "highlights": [
            "Add capacity exactly where you're stretched thin",
            "No need to build a full in-house team before you're ready",
            "Start with one role and expand as the business grows",
        ],
    },
    "agencies": {
        "title": "Agencies",
        "tagline": "Take on more client work without overextending your core team.",
        "description": "Client rosters don't grow at a steady pace, and neither should your team. We provide remote support for the account management, creative, or administrative work that piles up as you take on more clients, so your core team isn't stretched across too many accounts at once.",
        "highlights": [
            "Cover overflow work during busy client cycles",
            "Keep account and admin work moving without slowing delivery",
            "Scale support up or down as your client roster changes",
        ],
    },
    "saas-companies": {
        "title": "SaaS Companies",
        "tagline": "Support for growth without slowing down product.",
        "description": "Between customer support tickets, lead follow-up, and day-to-day operations, a lot of what keeps a SaaS business running has nothing to do with the product itself. A remote specialist can take on that operational load so your core team can stay focused on building.",
        "highlights": [
            "Customer support coverage without pulling engineers off product work",
            "Lead generation and follow-up handled consistently",
            "Operational support that scales with your user base",
        ],
    },
    "ecommerce-businesses": {
        "title": "E-commerce Businesses",
        "tagline": "Keep operations running as order volume grows.",
        "description": "Order volume rarely grows in a straight line, and neither does the support work behind it. From customer service to admin and marketing tasks, a remote specialist helps you keep pace during busy periods without carrying that overhead year-round.",
        "highlights": [
            "Customer service support during peak order periods",
            "Admin and fulfillment coordination support",
            "Marketing and content support that keeps pace with your catalog",
        ],
    },
    "real-estate-companies": {
        "title": "Real Estate Companies",
        "tagline": "Stay responsive to clients and listings.",
        "description": "Between showings, closings, and client communication, administrative work often gets pushed to the end of the day. A remote specialist can handle lead follow-up, scheduling, and coordination, so agents can stay focused on clients and closings instead of paperwork.",
        "highlights": [
            "Lead follow-up so inquiries don't go cold",
            "Listing and transaction coordination support",
            "Scheduling and client communication support",
        ],
    },
    "coaches-consultants": {
        "title": "Coaches & Consultants",
        "tagline": "Spend more time with clients, less on admin.",
        "description": "The parts of the business that don't involve clients directly — scheduling, inbox management, outreach — can quietly eat up hours every week. A remote specialist takes that admin off your plate so more of your time goes toward the work only you can do.",
        "highlights": [
            "Calendar and scheduling management",
            "Client outreach and follow-up support",
            "Day-to-day admin so you can focus on delivery",
        ],
    },
    "professional-services": {
        "title": "Professional Services",
        "tagline": "Reliable support behind the scenes.",
        "description": "Firms in professional services — legal, accounting, consulting, and similar fields — depend on protecting billable, client-facing time. A remote specialist can take on the administrative and operational work behind the scenes: scheduling, document preparation, client intake, and coordination, so that time stays protected and nothing falls through the cracks as the firm grows.",
        "highlights": [
            "Administrative and document support tailored to how your firm works",
            "Client intake and scheduling coordination",
            "Operational support that protects billable time",
        ],
    },
    "startups": {
        "title": "Startups",
        "tagline": "Get support without early full-time hires.",
        "description": "Early on, every hire matters, and a full-time role isn't always the right first move. A remote specialist lets you add support exactly where you need it — whether that's early sales outreach, operations, or admin — without committing to a large team before the business is ready for one.",
        "highlights": [
            "Add support without early full-time commitments",
            "Flexible enough to shift as priorities change",
            "A way to test what roles you actually need before hiring in-house",
        ],
    },
}

# ----------------------------------------------------------------------
# Talents pages -- for people interested in working with Flow Remote Ops
# ----------------------------------------------------------------------
CAREERS_PAGE = {
    "title": "Careers",
    "tagline": "Work with growing businesses as a remote specialist.",
    "paragraphs": [
        "Flow Remote Ops matches remote specialists to businesses that need support across sales, operations, administration, marketing, and technology. You're matched to work that fits your background, rather than a single generic assignment.",
        "Roles are remote-first. You'll work closely with a client business, with support from Flow Remote Ops along the way rather than being left to figure things out alone.",
    ],
    "highlights": [
        "Clear communication and reliable follow-through",
        "Comfortable working with international clients and teams",
        "Relevant experience in your category — sales, operations, marketing, or technology",
        "A self-directed way of working, without needing constant supervision",
    ],
    "highlights_heading": "What we look for",
}

# Categories shown as filter tags on the Careers page. OPEN_ROLES is
# intentionally empty -- add real postings here as {"title", "type",
# "category", "date"} dicts once you have actual openings. Never fake
# a listing just to fill the page.
CAREER_CATEGORIES = [
    "Sales & Business Development",
    "Operations & Administration",
    "Marketing & Creative",
    "Technology & Automation",
]
OPEN_ROLES = []

WORK_LIFE_BALANCE_PAGE = {
    "title": "Work-Life Balance",
    "tagline": "Remote work that respects your time.",
    "paragraphs": [
        "Remote work only works long-term if it's sustainable. Flow Remote Ops sets clear expectations around scope and availability up front, rather than leaving hours undefined or expecting round-the-clock availability.",
        "We look for engagements to be judged by the work delivered, not by time spent logged in. Full-time and part-time arrangements are both available, matched to what actually fits your availability.",
    ],
    "highlights": [
        "Clear scope and availability agreed on before you start",
        "Full-time and part-time arrangements available",
        "Support from Flow Remote Ops if something about an engagement isn't working",
    ],
    "highlights_heading": "How we approach it",
}

APPLICATION_STEPS = [
    {
        "title": "Submit your application",
        "description": "Fill out the Job Application Form with your background, relevant experience, and the type of role you're interested in.",
    },
    {
        "title": "Confirmation email",
        "description": "You'll get an email confirming we received your application, so you know it's in the queue.",
    },
    {
        "title": "Initial screening call",
        "description": "If your background looks like a fit, we'll reach out for a short call to learn more about your experience and what you're looking for.",
    },
    {
        "title": "Skills check",
        "description": "Depending on the role, you may be asked to complete a short skills-related task or assessment. Not every role requires this — we'll let you know if it applies.",
    },
    {
        "title": "Client interview",
        "description": "If it's a strong fit, you'll meet with the client business for a more in-depth conversation about the role.",
    },
    {
        "title": "Background check",
        "description": "Before an offer goes out, we verify employment history and other relevant details.",
    },
    {
        "title": "Offer & agreement",
        "description": "Once everything checks out, we'll send over the terms of the engagement for you to review and sign.",
    },
    {
        "title": "Onboarding",
        "description": "We'll walk you through how we work before you start, then introduce you to the client for a kickoff call.",
    },
]

JOB_APPLICATION_FORM = {
    "title": "Job Application Form",
    "tagline": "Tell us about your background and the kind of role you're looking for.",
    "form_id": "job-application-form",
    "fields": [
        {"type": "text", "name": "full_name", "label": "Full Name", "required": True},
        {"type": "email", "name": "email", "label": "Email", "required": True},
        {"type": "tel", "name": "phone", "label": "Phone Number", "required": False},
        {
            "type": "select", "name": "role_interest", "label": "Role you're interested in", "required": True,
            "options": ["Sales & Business Development", "Operations & Administration", "Marketing & Creative", "Technology & Automation", "Other"],
        },
        {"type": "text", "name": "portfolio_url", "label": "LinkedIn or Portfolio URL", "required": False, "placeholder": "linkedin.com/in/yourname"},
        {"type": "text", "name": "resume_url", "label": "Link to your resume/CV", "required": False, "placeholder": "Google Drive, Dropbox, etc."},
        {
            "type": "radio", "name": "availability", "label": "Availability", "required": False,
            "options": ["Full-time", "Part-time", "Either"],
        },
        {"type": "textarea", "name": "experience", "label": "Tell us about your relevant experience", "required": True, "rows": 4},
    ],
}

CANDIDATE_INQUIRY_FORM = {
    "title": "Candidate Inquiry Form",
    "tagline": "Have a question before applying? Ask here.",
    "form_id": "candidate-inquiry-form",
    "fields": [
        {"type": "text", "name": "full_name", "label": "Name", "required": True},
        {"type": "email", "name": "email", "label": "Email", "required": True},
        {"type": "textarea", "name": "question", "label": "Your question", "required": True, "rows": 4},
    ],
}

CANDIDATE_REFERRAL_FORM = {
    "title": "Candidate Referral Form",
    "tagline": "Know someone who'd be a great fit? Let us know.",
    "form_id": "candidate-referral-form",
    "fields": [
        {"type": "text", "name": "referrer_name", "label": "Your Name", "required": True},
        {"type": "email", "name": "referrer_email", "label": "Your Email", "required": True},
        {"type": "text", "name": "candidate_name", "label": "Candidate's Name", "required": True},
        {"type": "text", "name": "candidate_contact", "label": "Candidate's Email or Contact Info", "required": True},
        {"type": "textarea", "name": "referral_reason", "label": "Why are you referring them?", "required": False, "rows": 3},
    ],
}


# ----------------------------------------------------------------------
# Legal pages -- placeholder templates, not legal advice. Have these
# reviewed by a lawyer before relying on them.
# ----------------------------------------------------------------------
LEGAL_UPDATED_DATE = "September 2026"

TERMS_OF_SERVICE = {
    "title": "Terms of Service",
    "intro": "These Terms of Service (\"Terms\") govern your use of the Flow Remote Ops website. By using this website, you agree to these Terms. If you don't agree, please don't use the site.",
    "sections": [
        {
            "heading": "1. Use of This Website",
            "paragraphs": [
                "You may use this website for lawful purposes only, and in a way that doesn't infringe on anyone else's ability to use it.",
                "You agree not to attempt to disrupt, damage, or gain unauthorized access to this website or its underlying systems.",
            ],
        },
        {
            "heading": "2. Intellectual Property",
            "paragraphs": [
                "The content, branding, and materials on this website belong to Flow Remote Ops unless stated otherwise. You may not copy, reproduce, or repurpose them without our written permission.",
            ],
        },
        {
            "heading": "3. Third-Party Links",
            "paragraphs": [
                "This website may link to third-party sites we don't control. We aren't responsible for their content, policies, or practices.",
            ],
        },
        {
            "heading": "4. No Warranty",
            "paragraphs": [
                "This website is provided \"as is,\" without warranties of any kind. We don't guarantee it will be uninterrupted, error-free, or free of harmful components.",
            ],
        },
        {
            "heading": "5. Limitation of Liability",
            "paragraphs": [
                "To the extent permitted by law, Flow Remote Ops isn't liable for any indirect, incidental, or consequential damages arising from your use of this website.",
            ],
        },
        {
            "heading": "6. Changes to These Terms",
            "paragraphs": [
                "We may update these Terms from time to time. Continued use of the website after changes are posted means you accept the updated Terms.",
            ],
        },
        {
            "heading": "7. Governing Law",
            "paragraphs": [
                "These Terms are governed by the laws of [your jurisdiction] — replace this placeholder with wherever Flow Remote Ops is legally based.",
            ],
        },
    ],
}

PRIVACY_POLICY = {
    "title": "Privacy Policy",
    "intro": "This Privacy Policy explains how Flow Remote Ops collects, uses, and protects information from visitors to this website. By using this site, you agree to the practices described here.",
    "sections": [
        {
            "heading": "1. Information We Collect",
            "paragraphs": [
                "Information you provide directly, such as your name, email address, and business details, when you fill out a form on this site.",
                "Basic technical information collected automatically, such as browser type and pages visited, which helps us understand how the site is used.",
            ],
        },
        {
            "heading": "2. How We Use It",
            "paragraphs": [
                "To respond to inquiries submitted through the site and follow up on requests for a remote team.",
                "To understand how visitors use the site so we can improve it over time.",
            ],
        },
        {
            "heading": "3. Sharing of Information",
            "paragraphs": [
                "We don't sell your personal information. We may share it with service providers who help us operate the site (such as form or hosting providers), or when required by law.",
            ],
        },
        {
            "heading": "4. Data Security",
            "paragraphs": [
                "We take reasonable steps to protect information submitted through this site, though no method of transmission or storage is completely secure.",
            ],
        },
        {
            "heading": "5. Your Choices",
            "paragraphs": [
                "You can ask us to access, correct, or delete information you've submitted by contacting us directly.",
            ],
        },
        {
            "heading": "6. Changes to This Policy",
            "paragraphs": [
                "We may update this Privacy Policy from time to time. The date at the top of this page reflects the most recent update.",
            ],
        },
    ],
}

COOKIE_POLICY = {
    "title": "Cookie Policy",
    "intro": "This Cookie Policy explains how Flow Remote Ops uses cookies and similar technologies on this website.",
    "sections": [
        {
            "heading": "1. What Cookies Are",
            "paragraphs": [
                "Cookies are small files stored on your device when you visit a website. They help the site function properly and let us understand how it's used.",
            ],
        },
        {
            "heading": "2. How We Use Cookies",
            "paragraphs": [
                "Essential cookies that keep the site working correctly.",
                "Basic analytics cookies that help us understand which pages get used, so we can improve the site over time.",
            ],
        },
        {
            "heading": "3. Managing Cookies",
            "paragraphs": [
                "Most browsers let you block or delete cookies through their settings. Doing so may affect how parts of this site work.",
            ],
        },
        {
            "heading": "4. Changes to This Policy",
            "paragraphs": [
                "We may update this Cookie Policy from time to time. The date at the top of this page reflects the most recent update.",
            ],
        },
    ],
}


@app.route("/")
def index():
    """Render the landing page."""
    return render_template("index.html")


@app.route("/contact")
def contact():
    """Render the dedicated Build Your Remote Team / contact page."""
    return render_template("contact.html")


@app.route("/vision-and-mission")
def vision_mission():
    """Render the Vision & Mission page."""
    return render_template("vision_mission.html")


@app.route("/faq")
def faq():
    """Render the dedicated FAQ page."""
    return render_template("faq.html")


@app.route("/blog")
def blog():
    """Render the Blog landing page (no posts yet)."""
    return render_template("blog.html")


@app.route("/terms-of-service")
def terms_of_service():
    """Render the Terms of Service page."""
    return render_template("legal_page.html", updated=LEGAL_UPDATED_DATE, **TERMS_OF_SERVICE)


@app.route("/privacy-policy")
def privacy_policy():
    """Render the Privacy Policy page."""
    return render_template("legal_page.html", updated=LEGAL_UPDATED_DATE, **PRIVACY_POLICY)


@app.route("/cookie-policy")
def cookie_policy():
    """Render the Cookie Policy page."""
    return render_template("legal_page.html", updated=LEGAL_UPDATED_DATE, **COOKIE_POLICY)


@app.route("/services/<slug>")
def service_page(slug):
    """Render a dedicated page for one service category."""
    if slug not in SERVICE_PAGES:
        abort(404)
    return render_template("service_page.html", slug=slug, page=SERVICE_PAGES[slug])


@app.route("/who-we-help/<slug>")
def who_we_help_page(slug):
    """Render a dedicated page for one audience type."""
    if slug not in WHO_WE_HELP_PAGES:
        abort(404)
    return render_template("who_we_help_page.html", slug=slug, page=WHO_WE_HELP_PAGES[slug])


@app.route("/talents/careers")
def talents_careers():
    """Render the Careers page."""
    return render_template(
        "careers_page.html",
        page=CAREERS_PAGE,
        categories=CAREER_CATEGORIES,
        open_roles=OPEN_ROLES,
    )


@app.route("/talents/application-process")
def talents_application_process():
    """Render the Application Process page."""
    return render_template("talent_process_page.html", steps=APPLICATION_STEPS)


@app.route("/talents/work-life-balance")
def talents_work_life_balance():
    """Render the Work-Life Balance page."""
    return render_template("talent_info_page.html", page=WORK_LIFE_BALANCE_PAGE)


@app.route("/talents/job-application-form")
def talents_job_application_form():
    """Render the Job Application Form."""
    return render_template("talent_form_page.html", **JOB_APPLICATION_FORM)


@app.route("/talents/candidate-inquiry-form")
def talents_candidate_inquiry_form():
    """Render the Candidate Inquiry Form."""
    return render_template("talent_form_page.html", **CANDIDATE_INQUIRY_FORM)


@app.route("/talents/candidate-referral-form")
def talents_candidate_referral_form():
    """Render the Candidate Referral Form."""
    return render_template("talent_form_page.html", **CANDIDATE_REFERRAL_FORM)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")