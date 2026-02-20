from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

#This file manages the conversational coaching flow:
class PitchCoachFlow:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, api_key=os.getenv("OPENAI_API_KEY"))
        self.pitch_components = {
            "one_liner": None,
            "problem": None,
            "solution": None,
            "market": None,
            "business_model": None,
            "unique_value": None,
            "traction": None,
            "team": None,
            "ask": None
        }
        self.current_stage = "intro"
        self.history = []
        
    def start_conversation(self):
        """Start the coaching conversation"""
        welcome_message = """
        Hi there! I'm your AI Pitch Coach. I'm going to help you craft a compelling startup pitch 
        by guiding you through each key element step by step.
        
        Let's work on your startup pitch! Can you summarize your startup in one sentence?
        """
        self.current_stage = "one_liner"
        self.add_to_history("coach", welcome_message)
        return welcome_message
    
    def process_response(self, user_message):
        """Process the user's response based on the current stage"""
        self.add_to_history("user", user_message)
        
        # Store the user's response in the appropriate component
        if self.current_stage in self.pitch_components:
            self.pitch_components[self.current_stage] = user_message
        
        # Generate the next prompt based on the current stage
        next_prompt = self._get_next_prompt(self.current_stage, user_message)
        self.add_to_history("coach", next_prompt)
        
        # Move to the next stage
        self.current_stage = self._get_next_stage(self.current_stage)
        
        return next_prompt
    
    def _get_next_stage(self, current_stage):
        """Determine the next stage in the conversation flow"""
        stages = [
            "intro", "one_liner", "problem", "solution", 
            "market", "business_model", "unique_value", 
            "traction", "team", "ask", "summary"
        ]
        
        if current_stage not in stages:
            return "summary"
            
        current_index = stages.index(current_stage)
        if current_index + 1 < len(stages):
            return stages[current_index + 1]
        else:
            return "summary"
    
    def _get_next_prompt(self, current_stage, user_message):
        """Generate the next prompt based on the current stage and user message"""
        if current_stage == "intro":
            return "Let's work on your startup pitch! Can you summarize your startup in one sentence?"
            
        elif current_stage == "one_liner":
            return f"""
            That's a great start! Now, what's the core problem your {self._extract_product_type(user_message)} solves for users?
            
            Try to articulate this problem in a way that investors would immediately understand its significance.
            """
            
        elif current_stage == "problem":
            # Provide feedback on the problem statement
            problem_feedback = self._generate_feedback(
                user_message, 
                "problem statement",
                "clear, concise, and highlighting a significant pain point that customers face"
            )
            
            return f"""
            {problem_feedback}
            
            Now, tell me more about your solution. How does your product or service solve this problem?
            """
            
        elif current_stage == "solution":
            # Provide feedback on the solution
            solution_feedback = self._generate_feedback(
                user_message, 
                "solution description",
                "specific, differentiated, and clearly addressing the problem you identified"
            )
            
            return f"""
            {solution_feedback}
            
            Let's talk about your target market. Who are your primary customers, and how large is this market?
            """
            
        elif current_stage == "market":
            # Provide feedback on the market description
            market_feedback = self._generate_feedback(
                user_message, 
                "market description",
                "specific, sizeable, and showing good growth potential"
            )
            
            return f"""
            {market_feedback}
            
            Great! Now, explain your business model. How do you make money?
            """
            
        elif current_stage == "business_model":
            # Provide feedback on the business model
            model_feedback = self._generate_feedback(
                user_message, 
                "business model",
                "clear, scalable, and demonstrating strong unit economics"
            )
            
            return f"""
            {model_feedback}
            
            What makes your approach unique? What's your unique value proposition or competitive advantage?
            """
            
        elif current_stage == "unique_value":
            # Provide feedback on the unique value proposition
            uvp_feedback = self._generate_feedback(
                user_message, 
                "unique value proposition",
                "compelling, defensible, and clearly differentiating you from competitors"
            )
            
            return f"""
            {uvp_feedback}
            
            Do you have any traction or early validation? (e.g., customers, revenue, partnerships, pilot programs)
            """
            
        elif current_stage == "traction":
            # Provide feedback on the traction
            traction_feedback = self._generate_feedback(
                user_message, 
                "traction description",
                "specific, showing momentum, and validating market interest"
            )
            
            return f"""
            {traction_feedback}
            
            Tell me briefly about your team. What makes your team uniquely qualified to execute on this vision?
            """
            
        elif current_stage == "team":
            # Provide feedback on the team
            team_feedback = self._generate_feedback(
                user_message, 
                "team description",
                "highlighting relevant expertise, domain knowledge, and prior successes"
            )
            
            return f"""
            {team_feedback}
            
            Finally, what are you asking for? (Investment amount, specific help, partnerships, etc.)
            """
            
        elif current_stage == "ask":
            # Provide feedback on the ask
            ask_feedback = self._generate_feedback(
                user_message, 
                "ask",
                "clear, specific, and appropriate for your stage"
            )
            
            # Generate the complete pitch
            complete_pitch = self._generate_complete_pitch()
            
            return f"""
            {ask_feedback}
            
            Fantastic! We've now covered all the key elements of a compelling pitch. Here's a synthesized version of your pitch based on everything you've shared:
            
            {complete_pitch}
            
            Would you like to:
            1. Refine any specific part of your pitch
            2. Practice answering investor questions
            3. Get feedback on the overall pitch clarity and persuasiveness
            """
            
        else:  # summary or unknown stage
            return """
            Is there any specific part of your pitch you'd like to refine further? 
            Or would you like to practice answering potential investor questions?
            """
    
    def _generate_feedback(self, user_input, component_name, ideal_characteristics):
        """Generate constructive feedback on a pitch component"""
        positive_phrases = [
            "That's excellent!",
            "Really strong!",
            "Great point!",
            "I like how you've articulated this.",
            "You've done a nice job explaining this.",
            "That's compelling!",
            "Well done!"
        ]
        
        constructive_phrases = [
            "Consider strengthening this by",
            "You might enhance this further by",
            "This is good, and you could make it even stronger by",
            "Another approach might be to",
            "Have you thought about",
            "One suggestion would be to"
        ]
        
        # Use the LLM to generate actual feedback based on the content
        prompt = f"""
        Analyze this {component_name} for a startup pitch:
        "{user_input}"
        
        A great {component_name} should be {ideal_characteristics}.
        
        Provide constructive feedback with:
        1. A specific positive aspect of what was shared (using a warm, encouraging tone)
        2. One specific, actionable suggestion to make it stronger (be specific, not generic)
        
        Keep your response under 3 sentences and maintain a supportive, coaching tone.
        """
        
        try:
            response = self.llm.invoke(prompt)
            feedback = response.content
            return feedback
        except Exception as e:
            # Fallback if LLM call fails
            import random
            positive = random.choice(positive_phrases)
            constructive = random.choice(constructive_phrases)
            return f"{positive} {constructive} making it more {ideal_characteristics.split(' and ')[0]}."
    
    def _extract_product_type(self, one_liner):
        """Extract the product type from the one-liner description"""
        if "app" in one_liner.lower():
            return "app"
        elif "platform" in one_liner.lower():
            return "platform"
        elif "service" in one_liner.lower():
            return "service"
        elif "AI" in one_liner or "artificial intelligence" in one_liner.lower():
            return "AI solution"
        else:
            return "solution"
    
    def _generate_complete_pitch(self):
        """Generate a complete pitch based on all components"""
        # Combine all pitch components into a coherent pitch
        components = self.pitch_components
        
        pitch = f"""
        {components['one_liner']}
        
        Problem: {components['problem']}
        
        Solution: {components['solution']}
        
        Market: {components['market']}
        
        Business Model: {components['business_model']}
        
        Unique Value: {components['unique_value']}
        """
        
        # Add optional components if they contain content
        if components['traction'] and components['traction'].strip():
            pitch += f"\n\nTraction: {components['traction']}"
            
        if components['team'] and components['team'].strip():
            pitch += f"\n\nTeam: {components['team']}"
            
        if components['ask'] and components['ask'].strip():
            pitch += f"\n\nAsk: {components['ask']}"
        
        return pitch
    
    def get_investor_questions(self):
        """Generate potential investor questions based on the pitch"""
        # Combine pitch components for context
        pitch_context = "\n".join([
            f"{k}: {v}" for k, v in self.pitch_components.items() 
            if v and v.strip()
        ])
        
        prompt = f"""
        Based on this startup pitch:
        
        {pitch_context}
        
        Generate 5 challenging but realistic investor questions that probe potential weaknesses or areas needing clarification. For each question, provide a brief tip on how to answer effectively.
        
        Format as:
        1. [Question 1]
           Tip: [Answering guidance]
        2. [Question 2]
           Tip: [Answering guidance]
        ...and so on
        """
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            # Fallback questions if LLM call fails
            return """
            1. How do you plan to acquire your first 100 customers?
               Tip: Be specific about your go-to-market strategy and early traction channels.
               
            2. What happens if a larger competitor copies your solution?
               Tip: Focus on your unique advantages, speed of execution, and barriers to entry.
               
            3. How did you arrive at your market size estimate?
               Tip: Show your calculation methodology and cite credible sources.
               
            4. What are your unit economics and path to profitability?
               Tip: Demonstrate understanding of your costs, pricing strategy, and timeline to breakeven.
               
            5. Why is now the right time for this solution?
               Tip: Highlight market timing factors, technology enablers, or regulatory changes that make this the perfect moment.
            """
    
    def get_pitch_clarity_feedback(self):
        """Generate feedback on the overall pitch clarity and persuasiveness"""
        # Combine pitch components for context
        pitch_context = "\n".join([
            f"{k}: {v}" for k, v in self.pitch_components.items() 
            if v and v.strip()
        ])
        
        prompt = f"""
        Evaluate this startup pitch for clarity, persuasiveness, and investor appeal:
        
        {pitch_context}
        
        Provide constructive feedback in these categories:
        1. Clarity & Simplicity: How clearly are complex concepts explained?
        2. Persuasiveness: How compelling is the overall narrative?
        3. Logical Flow: How well do the pieces connect?
        4. Memorability: What will investors remember?
        5. Improvement Areas: What specific changes would make this pitch stronger?
        
        Keep each category to 1-2 sentences with specific, actionable advice. Maintain a supportive, coaching tone.
        """
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            # Fallback feedback if LLM call fails
            return """
            1. Clarity & Simplicity: The pitch explains the concept well, but try using more concrete examples to illustrate how your solution works in practice.
            
            2. Persuasiveness: You've outlined a compelling opportunity, though strengthening the urgency factor would help investors feel the need to act now.
            
            3. Logical Flow: The narrative flows naturally from problem to solution, but explicitly connecting your team's expertise to the specific challenges would strengthen the story.
            
            4. Memorability: Your unique value proposition stands out, though creating a simple one-line tagline could make it even more memorable.
            
            5. Improvement Areas: Quantify your claims more specifically with metrics and data points. Also, clarify exactly how you'll use the investment funds with specific milestones.
            """
    
    def add_to_history(self, speaker, message):
        """Add a message to the conversation history"""
        self.history.append({
            "speaker": speaker,
            "message": message
        })
    
    def get_history(self):
        """Get the complete conversation history"""
        return self.history