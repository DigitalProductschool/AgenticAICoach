import os
from .crew import build_crew, run_structure

def main():
  if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY is not set")

  crew_parts = build_crew()
  context = {}
  stage = "one_liner"

  while True:
    msg = input(f"[{stage}] Your input: ").strip()
    if msg.lower() in {"exit", "quit"}:
      break

    res = run_structure(crew_parts, stage=stage, context=context, user_message=msg, audience="VC", funding_stage="pre-seed")
    print("\nCoach:\n", res, "\n")

if __name__ == "__main__":
  main()