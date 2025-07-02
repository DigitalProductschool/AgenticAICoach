import os
from pydantic import BaseModel
from typing import List

import chainlit as cl
from crewai.flow.flow import Flow, listen, start
from crews.visual_crew.visual_crew import VisualCrew
from crews.content_crew.content_crew import ContentCrew
from crews.narrative_crew.narrative_crew import NarrativeCrew
from crews.messaging_crew.messaging_crew import MessagingCrew

greeting_message = \
"""
I'm your AI Storytelling & Branding Coach, here to help you craft a brand narrative that inspires, connects, and stands out.
So, let's get started!
Please share your general idea or vision for your brand, and we'll begin the journey of shaping your brand's story together.
"""

class BrandState(BaseModel):
    mission: str = ""
    vision: str = ""
    values: str = ""
    target_audience_pain_points: str = ""
    core_story: str = ""
    messaging_feedback: str = ""
    website_copy: str = ""
    visual_guidelines: str = ""
    refined_message: str = ""
    taglines: List[str] = []
    slogans: List[str] = []

class BrandCoachFlow(Flow[BrandState]):

    @start()
    def improve_narrative(self, general_idea: str = None) -> str:
        crew = NarrativeCrew().crew()
        res = crew.kickoff(inputs={"general_idea": general_idea})

        self.state.mission = res['mission']
        self.state.vision = res['vision']
        self.state.values = res['values']
        self.state.target_audience_pain_points = res['target_audience_pain_points']
        self.state.core_story = res['final_narrative']

        return self.state

    @listen(improve_narrative)
    def improve_messaging(self):
        crew = MessagingCrew().crew()

        inputs = {
            "mission": self.state.mission,
            "vision": self.state.vision,
            "values": self.state.values,
            "target_audience_pain_points": self.state.target_audience_pain_points,
            "core_story": self.state.core_story
        }

        res = crew.kickoff(inputs=inputs)
        self.state.refined_message = res['refined_message']
        self.state.taglines = res['taglines']
        self.state.slogans = res['slogans']

        return self.state

    @listen(improve_messaging)
    def generate_content(self):
        crew = ContentCrew().crew()

        inputs = {
            "mission": self.state.mission,
            "vision": self.state.vision,
            "values": self.state.values,
            "target_audience_pain_points": self.state.target_audience_pain_points,
            "core_story": self.state.core_story,
            "refined_message": self.state.refined_message,
            "taglines": self.state.taglines,
            "slogans": self.state.slogans
        }
        res = crew.kickoff(inputs=inputs)

        self.state.website_copy = res.raw
        return self.state

    @listen(generate_content)
    def define_visuals(self):
        crew = VisualCrew().crew()

        inputs = {
            "website_copy": self.state.website_copy,
        }
        res = crew.kickoff(inputs=inputs)

        self.state.visual_guidelines = res.raw
        return res.raw

flow = BrandCoachFlow()

@cl.on_chat_start
async def greet():
    await cl.Message(greeting_message).send()

@cl.on_message
async def handle(msg: cl.Message):

    flow.improve_narrative(general_idea=msg.content)
    flow.improve_messaging()
    flow.generate_content()
    flow.define_visuals()

    await cl.Message(
        content= \
        f"""
        Thank you for sharing your brand vision! Here's a summary of the key elements we've developed together:
        **Mission:** {flow.state.mission}
        **Vision:** {flow.state.vision}
        **Values:** {flow.state.values}
        **Target Audience Pain Points:** {flow.state.target_audience_pain_points}
        **Core Story:** {flow.state.core_story}
        **Refined Message:** {flow.state.refined_message}
        **Taglines:** {', '.join(flow.state.taglines)}
        **Slogans:** {', '.join(flow.state.slogans)}
        **Website Copy:** {flow.state.website_copy}
        **Visual Guidelines:** {flow.state.visual_guidelines}
        **Messaging Feedback:** {flow.state.messaging_feedback}
        """,
    ).send()