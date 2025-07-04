"""
Test data for Growth Hacking Coach tests.
"""

# Sample user messages for testing
SAMPLE_USER_MESSAGES = [
    "How can I grow my startup?",
    "I need help with user engagement for my mobile app.",
    "What are the best viral marketing techniques for a SaaS product?",
    "How do I optimize my content for better conversion rates?",
    "What growth metrics should I track for my e-commerce business?",
    "How can I leverage social media for rapid growth?",
    "I'm struggling with customer retention. Any advice?",
    "What are some low-cost growth hacking strategies for a bootstrapped startup?",
    "How can I improve my product's viral coefficient?",
    "What are the most effective referral program structures?"
]

# Sample conversation history for testing
SAMPLE_CONVERSATION_HISTORY = [
    [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there! How can I help you with growth hacking today?"}
    ],
    [
        {"role": "user", "content": "I need help with my startup"},
        {"role": "assistant", "content": "I'd be happy to help with your startup! To provide the most relevant advice, could you tell me a bit more about your startup? What industry are you in, what's your target audience, and what specific growth challenges are you facing?"},
        {"role": "user", "content": "It's a fintech app for young professionals"}
    ],
    [
        {"role": "user", "content": "How can I improve user engagement?"},
        {"role": "assistant", "content": "To improve user engagement, I recommend focusing on these key strategies: 1) Enhance your onboarding experience to demonstrate value quickly, 2) Implement personalized notifications to bring users back, 3) Add gamification elements to make the experience more enjoyable, and 4) Create content that addresses your users' specific pain points."},
        {"role": "user", "content": "Can you elaborate on gamification?"}
    ]
]

# Sample API responses for testing
SAMPLE_API_RESPONSES = [
    {
        "response": "To grow your startup effectively, I recommend focusing on these key areas:\n\n1. **Product-Market Fit**: Ensure your product truly solves a pain point for your target audience.\n\n2. **Customer Acquisition Channels**: Identify 2-3 channels that work best for your specific business and double down on them.\n\n3. **Retention Strategy**: It's cheaper to keep existing customers than acquire new ones. Implement a solid onboarding process and regular engagement touchpoints.\n\n4. **Growth Metrics**: Track key metrics like CAC (Customer Acquisition Cost), LTV (Lifetime Value), and conversion rates at each funnel stage.\n\nWould you like me to dive deeper into any of these areas based on your specific business?"
    },
    {
        "response": "For improving user engagement in your mobile app, consider these strategies:\n\n1. **Personalized Onboarding**: Create a tailored first-time user experience that highlights the most relevant features.\n\n2. **Push Notification Strategy**: Use behavior-triggered notifications rather than time-based ones.\n\n3. **In-app Messaging**: Communicate new features and benefits contextually within the app.\n\n4. **Gamification Elements**: Add progress bars, achievements, or points systems to encourage continued usage.\n\n5. **Feature Discovery**: Gradually introduce advanced features to prevent overwhelming users.\n\nCould you tell me more about your app's current engagement metrics so I can provide more specific advice?"
    }
]

# Sample error messages for testing
SAMPLE_ERROR_MESSAGES = [
    "Connection refused",
    "Internal Server Error",
    "Timeout while connecting to server",
    "Invalid request format",
    "API key not provided or invalid"
]
