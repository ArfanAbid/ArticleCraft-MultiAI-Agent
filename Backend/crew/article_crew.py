from crewai import Crew, Process
from crew.agents import researcher, writer, proof_reader
from crew.tasks import research_task, write_task, proof_read_task


def create_crew() -> Crew:
    return Crew(
        agents=[researcher, writer, proof_reader],
        tasks=[research_task, write_task, proof_read_task],
        process=Process.sequential
    )
