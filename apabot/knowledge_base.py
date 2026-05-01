"""Paper-aligned ASD support knowledge for the fallback assistant."""

ASD_KNOWLEDGE = {
    "what_is_asd": (
        "Autism spectrum disorder (ASD) is a neurodevelopmental condition associated "
        "with differences in social communication, restricted interests, repetitive "
        "behaviors, and sensory responses."
    ),
    "asd_support": (
        "Support commonly focuses on communication, emotional regulation, daily "
        "functioning, and anxiety management. A chatbot can provide conversational "
        "practice and emotional support, but it is not a substitute for clinicians, "
        "caregivers, or therapists."
    ),
    "hypersensitivity": (
        "Sensory hypersensitivity, including strong reactions to sound or visual input, "
        "is often reported in autistic individuals and can affect social and academic life."
    ),
    "limitations": (
        "The APABOT paper presents a prototype and explicitly recommends further "
        "validation in real clinical settings with ethical clearance."
    ),
}

FAQ_PATTERNS = {
    "what is asd": "what_is_asd",
    "define asd": "what_is_asd",
    "autism spectrum disorder": "what_is_asd",
    "how can asd be supported": "asd_support",
    "how to support asd": "asd_support",
    "sensory sensitivity": "hypersensitivity",
    "hypersensitivity": "hypersensitivity",
    "limitations": "limitations",
    "clinical validation": "limitations",
}
