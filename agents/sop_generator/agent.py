from .models import SOPRequest, SOPResponse

def generate_sop(request: SOPRequest) -> SOPResponse:
    desc = request.process_description.strip()

    if not desc:
        desc = "Unnamed process"

    title = f"SOP: {desc[:60]}"

    return SOPResponse(
        title=title,
        purpose=f"Define a clear, repeatable process for: {desc}",
        scope="This SOP applies to all team members involved in this process.",
        responsibilities=[
            "Process Owner: Ensures the SOP is followed and updated.",
            "Team Members: Execute the steps as described.",
            "Supervisor: Reviews outcomes and KPIs regularly."
        ],
        materials=[
            "Relevant tools, systems, or software required for the process.",
            "Access credentials or permissions, if applicable.",
            "Documentation templates or forms."
        ],
        steps=[
            "Step 1: Gather all necessary inputs and prerequisites.",
            "Step 2: Execute the core actions described in the process.",
            "Step 3: Validate outputs and check for errors or inconsistencies.",
            "Step 4: Document results and update tracking systems.",
            "Step 5: Escalate issues or deviations to the supervisor if needed."
        ],
        kpis=[
            "On-time completion rate of the process.",
            "Error or rework rate.",
            "Cycle time from start to finish.",
            "Compliance with documentation requirements."
        ],
        risks=[
            "Incomplete or incorrect inputs leading to errors.",
            "Lack of documentation causing confusion or rework.",
            "Delays due to unclear responsibilities.",
            "Non-compliance with regulatory or internal standards."
        ],
        version="v1.0",
        notes="This SOP was auto-generated based on a high-level process description. It should be reviewed and adapted."
    )
