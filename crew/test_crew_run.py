from crew_config import get_crew

if __name__ == "__main__":
    crew = get_crew()

    test_input = "We need a frontend React developer with good UX/UI skills"
    result = crew.run(test_input)
    
    print(" Final Output from Crew:")
    print(result)
