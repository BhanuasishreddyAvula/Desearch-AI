"""Multi-Agent Orchestrator executing sequential agent workflows."""

import time

from app.agents.planner.service import PlannerService
from app.agents.research.service import ResearchService
from app.agents.reviewer.service import ReviewerService
from app.agents.writer.service import WriterService
from app.core.exceptions import AppException
from app.observability.events import SystemEvents
from app.observability.logger import get_app_logger
from app.orchestrator.models import AgentExecution, WorkflowResult
from app.orchestrator.workflow import WorkflowStatus, WorkflowStep

logger = get_app_logger("orchestrator")


class MultiAgentOrchestrator:
    """Central orchestrator coordinating sequential AI agent execution."""

    def __init__(
        self,
        planner_service: PlannerService,
        research_service: ResearchService,
        writer_service: WriterService,
        reviewer_service: ReviewerService,
    ) -> None:
        self.planner_service = planner_service
        self.research_service = research_service
        self.writer_service = writer_service
        self.reviewer_service = reviewer_service

    def run_workflow(self, session_id: str, query: str) -> WorkflowResult:
        """Coordinate sequential execution of Planner Agent, Research Agent, Writer Agent, and Reviewer Agent."""
        workflow_start_time = time.perf_counter()
        executions: list[AgentExecution] = []

        logger.event(
            SystemEvents.APPLICATION_STARTED,
            f"Workflow Started | Session: {session_id} | Query: '{query[:60]}...'",
        )

        try:
            # ------------------------------------------------------------------
            # Step 1: Execute Planner Agent
            # ------------------------------------------------------------------
            logger.info("Planner Started | Session: %s", session_id)
            planner_start = time.perf_counter()

            planner_result = self.planner_service.create_plan(session_id)
            planner_duration = (time.perf_counter() - planner_start) * 1000.0

            logger.info(
                "Planner Completed | Session: %s | Duration: %.2fms",
                session_id,
                planner_duration,
            )
            executions.append(
                AgentExecution(
                    agent_name="PlannerAgent",
                    step=WorkflowStep.PLANNING,
                    status=WorkflowStatus.COMPLETED,
                    execution_time_ms=planner_duration,
                    details={"tasks_count": len(planner_result.tasks)},
                )
            )

            # ------------------------------------------------------------------
            # Step 2: Execute Research Agent
            # ------------------------------------------------------------------
            logger.info("Research Started | Session: %s", session_id)
            research_start = time.perf_counter()

            research_result = self.research_service.execute_research(
                session_id, planner_result
            )
            research_duration = (time.perf_counter() - research_start) * 1000.0

            logger.info(
                "Research Completed | Session: %s | Duration: %.2fms",
                session_id,
                research_duration,
            )
            executions.append(
                AgentExecution(
                    agent_name="ResearchAgent",
                    step=WorkflowStep.RESEARCHING,
                    status=WorkflowStatus.COMPLETED,
                    execution_time_ms=research_duration,
                    details={
                        "evidence_count": len(research_result.evidence_items),
                        "tools_executed": research_result.tools_executed,
                    },
                )
            )

            # ------------------------------------------------------------------
            # Step 3: Execute Writer Agent
            # ------------------------------------------------------------------
            logger.info("Writer Started | Session: %s", session_id)
            writer_start = time.perf_counter()

            report_result = self.writer_service.create_report(
                session_id, planner_result, research_result
            )
            writer_duration = (time.perf_counter() - writer_start) * 1000.0

            logger.info(
                "Writer Completed | Session: %s | Duration: %.2fms",
                session_id,
                writer_duration,
            )
            executions.append(
                AgentExecution(
                    agent_name="WriterAgent",
                    step=WorkflowStep.WRITING,
                    status=WorkflowStatus.COMPLETED,
                    execution_time_ms=writer_duration,
                    details={
                        "word_count": report_result.metadata.word_count,
                        "sections_count": report_result.metadata.sections_count,
                    },
                )
            )

            # ------------------------------------------------------------------
            # Step 4: Execute Reviewer Agent
            # ------------------------------------------------------------------
            logger.info("Reviewer Started | Session: %s", session_id)
            reviewer_start = time.perf_counter()

            review_result = self.reviewer_service.evaluate_report(
                session_id, planner_result, research_result, report_result
            )
            reviewer_duration = (time.perf_counter() - reviewer_start) * 1000.0

            logger.info(
                "Reviewer Completed | Session: %s | Duration: %.2fms | Approved: %s",
                session_id,
                reviewer_duration,
                review_result.approved,
            )
            executions.append(
                AgentExecution(
                    agent_name="ReviewerAgent",
                    step=WorkflowStep.REVIEWING,
                    status=WorkflowStatus.COMPLETED,
                    execution_time_ms=reviewer_duration,
                    details={
                        "approved": review_result.approved,
                        "overall_score": review_result.overall_score,
                    },
                )
            )

            # ------------------------------------------------------------------
            # Step 5: Aggregate Workflow Results
            # ------------------------------------------------------------------
            total_duration = (
                time.perf_counter() - workflow_start_time
            ) * 1000.0
            logger.event(
                SystemEvents.APPLICATION_STOPPED,
                f"Workflow Completed | Session: {session_id} | Total Duration: {total_duration:.2f}ms",
            )

            return WorkflowResult(
                session_id=session_id,
                status=WorkflowStatus.COMPLETED,
                planner_result=planner_result,
                research_result=research_result,
                report_result=report_result,
                review_result=review_result,
                executions=executions,
                total_execution_time_ms=total_duration,
            )

        except Exception as exc:
            total_duration = (
                time.perf_counter() - workflow_start_time
            ) * 1000.0
            logger.exception(
                "Workflow Failed | Session: %s | Total Duration: %.2fms | Error: %s",
                session_id,
                total_duration,
                str(exc),
            )
            if isinstance(exc, AppException):
                raise
            raise AppException(
                message=f"Multi-agent workflow execution failed: {str(exc)}",
                error_code="WORKFLOW_EXECUTION_ERROR",
            ) from exc
