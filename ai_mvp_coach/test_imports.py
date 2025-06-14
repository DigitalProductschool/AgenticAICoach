"""
Test script to verify import resolution
"""
# These imports should work without warnings
try:
    import crewai  # type: ignore
    import langchain_groq  # type: ignore
    import dotenv  # type: ignore
    import groq  # type: ignore
    print("All imports successful!")
except ImportError as e:
    print(f"Import error: {e}")
