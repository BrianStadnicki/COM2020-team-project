# Agile Development Workflow

## Tools

We have chosen to utilise GitHub for managing our repository and issue management.

We are using a GitHub Project with GitHub Issues, to manage tasks.

## Scrumboard / Issues

Our scrumboard allows us to view all issues (complete, in progress, and backlogged) visually within GitHub.

This allows us to store issues for both Sprint 1 and 2. Issues are further divided by stories.

Sprint 1 Stories
- Seller - bundles
- Seller - forecasting
- Consumer - bundles
- Consumer - reservations
- Demo - data
- Overall - design (more general tasks, most documentation issues belong here)

Each issue can belong in one of five progress columns:
- **Backlog** (issues begin here)
- **Ready** (when all prerequisites for an issue are complete, it moves here)
- **In progress** (current issues being worked on)
- **Review** (when an issue is ready for review)
- **Done** (completed issues)

Issues are created by either the scrum master (Brian) or the project lead (Ben). Each issue has several attributes:
- Title and Issue ID
- Description with further task breakdown
- Assignees
- Labels (e.g. documentatio, enhancement)
- Milestone (e.g. Sprint 1, Sprint 2)
- Relationships (Issues block and can block other issues)
- Development branch (optional)

Issues that are blocked by other issues cannot be worked on and belong in the Backlog.

## Code / Review Workflow

Code workflow:
- Create/checkout to a new branch for the issue
- Commits contain the issue number for easy tracking
- Merge the sprint branch into current branch to avoid merge conflicts.
- Create a pull request and assign reviewers

For a pull request to be merged, it must be reviewed by at least one other team member.

- A team member will review the code and either approve or reject it with appropriate comments or changes.
- This will continue with code changes until it is accepted and merged.