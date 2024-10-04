from crewai import Crew

def main():
    crew = Crew(
        config_path="config/agents.yaml", 
        task_config_path="config/tasks.yaml"
    )
    
    result = crew.run()
    print(result)

if __name__ == "__main__":
    main()
