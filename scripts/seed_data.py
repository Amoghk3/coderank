import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import asyncio
import uuid

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.security import hash_password

from app.models.user import User
from app.models.problem import Problem
from app.models.language import Language
from app.models.test_case import TestCase
from app.models.enums import (
    UserRole,
    ProblemDifficulty,
)


async def seed_users(db):

    users = [
        {
            "email": "admin@test.com",
            "username": "admin",
            "password": "Admin123!",
            "role": UserRole.ADMIN,
        },
        {
            "email": "user@test.com",
            "username": "user",
            "password": "User123!",
            "role": UserRole.USER,
        },
    ]

    for item in users:

        existing = await db.execute(
            select(User).where(
                User.email == item["email"]
            )
        )

        if existing.scalar_one_or_none():
            print(f"  ⏭  User already exists: {item['email']}")
            continue

        db.add(
            User(
                id=uuid.uuid4(),
                email=item["email"],
                username=item["username"],
                password_hash=hash_password(
                    item["password"]
                ),
                role=item["role"],
                is_active=True,
            )
        )

        print(f"  ✅ Created user: {item['email']}")

    await db.commit()


async def seed_languages(db):

    languages = [
        {
            "name": "python",
            "version": "3.12",
            "docker_image": "python:3.12-slim",
            "compile_command": None,
            "run_command": "python /code/main.py",
        },
        {
            "name": "javascript",
            "version": "20",
            "docker_image": "node:20-alpine",
            "compile_command": None,
            "run_command": "node /code/main.js",
        },
    ]

    for item in languages:

        existing = await db.execute(
            select(Language).where(
                Language.name == item["name"]
            )
        )

        if existing.scalar_one_or_none():
            print(f"  ⏭  Language already exists: {item['name']}")
            continue

        db.add(
            Language(
                id=uuid.uuid4(),
                name=item["name"],
                version=item["version"],
                docker_image=item["docker_image"],
                compile_command=item["compile_command"],
                run_command=item["run_command"],
                time_limit=2,
                memory_limit=256,
                is_active=True,
            )
        )

        print(f"  ✅ Created language: {item['name']} {item['version']}")

    await db.commit()


async def seed_problems(db):

    problems_data = [
        {
            "title": "Two Sum",
            "slug": "two-sum",
            "difficulty": ProblemDifficulty.EASY,
            "statement": (
                "Given an array of integers nums and an integer target, "
                "return indices of the two numbers such that they add up to target."
            ),
            "input_format": (
                "First line: n (size of array)\n"
                "Second line: n space-separated integers\n"
                "Third line: target integer"
            ),
            "output_format": "Two space-separated indices",
            "sample_input": "4\n2 7 11 15\n9",
            "sample_output": "0 1",
            "test_cases": [
                ("4\n2 7 11 15\n9", "0 1", False),
                ("3\n3 2 4\n6", "1 2", False),
                ("5\n1 5 3 7 2\n8", "1 2", True),
            ],
        },
        {
            "title": "Palindrome Number",
            "slug": "palindrome-number",
            "difficulty": ProblemDifficulty.EASY,
            "statement": (
                "Given an integer x, return true if x is a palindrome, "
                "and false otherwise."
            ),
            "input_format": "A single integer x",
            "output_format": "true or false",
            "sample_input": "121",
            "sample_output": "true",
            "test_cases": [
                ("121", "true", False),
                ("-121", "false", False),
                ("12321", "true", True),
            ],
        },
        {
            "title": "Valid Parentheses",
            "slug": "valid-parentheses",
            "difficulty": ProblemDifficulty.EASY,
            "statement": (
                "Given a string s containing just the characters "
                "'(', ')', '{', '}', '[' and ']', determine if the "
                "input string is valid."
            ),
            "input_format": "A single string of brackets",
            "output_format": "true or false",
            "sample_input": "()[]{}",
            "sample_output": "true",
            "test_cases": [
                ("()[]{}", "true", False),
                ("(]", "false", False),
                ("{[()]()}", "true", True),
            ],
        },
        {
            "title": "Longest Substring Without Repeating Characters",
            "slug": "longest-substring",
            "difficulty": ProblemDifficulty.MEDIUM,
            "statement": (
                "Given a string s, find the length of the longest substring "
                "without repeating characters."
            ),
            "input_format": "A single string s",
            "output_format": "An integer representing the length",
            "sample_input": "abcabcbb",
            "sample_output": "3",
            "test_cases": [
                ("abcabcbb", "3", False),
                ("bbbbb", "1", False),
                ("pwwkew", "3", True),
            ],
        },
        {
            "title": "Merge Intervals",
            "slug": "merge-intervals",
            "difficulty": ProblemDifficulty.MEDIUM,
            "statement": (
                "Given an array of intervals where intervals[i] = [start_i, end_i], "
                "merge all overlapping intervals."
            ),
            "input_format": (
                "First line: n (number of intervals)\n"
                "Next n lines: two space-separated integers (start end)"
            ),
            "output_format": "Merged intervals, one per line",
            "sample_input": "4\n1 3\n2 6\n8 10\n15 18",
            "sample_output": "1 6\n8 10\n15 18",
            "test_cases": [
                ("4\n1 3\n2 6\n8 10\n15 18", "1 6\n8 10\n15 18", False),
                ("2\n1 4\n4 5", "1 5", False),
                ("3\n1 4\n2 3\n5 8", "1 4\n5 8", True),
            ],
        },
    ]

    created_problems = []

    for item in problems_data:

        existing = await db.execute(
            select(Problem).where(
                Problem.slug == item["slug"]
            )
        )

        problem = existing.scalar_one_or_none()

        if problem:
            print(f"  ⏭  Problem already exists: {item['title']}")
            created_problems.append(
                (problem, item["test_cases"])
            )
            continue

        problem = Problem(
            id=uuid.uuid4(),
            title=item["title"],
            slug=item["slug"],
            difficulty=item["difficulty"],
            statement=item["statement"],
            input_format=item["input_format"],
            output_format=item["output_format"],
            sample_input=item["sample_input"],
            sample_output=item["sample_output"],
            time_limit_ms=2000,
            memory_limit_mb=128,
        )

        db.add(problem)

        print(f"  ✅ Created problem: {item['title']}")

        created_problems.append(
            (problem, item["test_cases"])
        )

    await db.commit()

    return created_problems


async def seed_test_cases(db, problems_with_cases):

    for problem, cases in problems_with_cases:

        existing = await db.execute(
            select(TestCase).where(
                TestCase.problem_id == problem.id
            )
        )

        if existing.scalars().first():
            print(f"  ⏭  Test cases already exist for: {problem.title}")
            continue

        for input_data, expected_output, is_hidden in cases:

            db.add(
                TestCase(
                    id=uuid.uuid4(),
                    problem_id=problem.id,
                    input_data=input_data,
                    expected_output=expected_output,
                    is_hidden=is_hidden,
                    points=10,
                )
            )

        print(f"  ✅ Created {len(cases)} test cases for: {problem.title}")

    await db.commit()


async def main():

    print("\n🌱 Seeding database...\n")

    async with AsyncSessionLocal() as db:

        print("👤 Users")
        await seed_users(db)

        print("\n💻 Languages")
        await seed_languages(db)

        print("\n📝 Problems")
        problems_with_cases = await seed_problems(db)

        print("\n🧪 Test Cases")
        await seed_test_cases(db, problems_with_cases)

    print("\n✅ Seed data loaded successfully!\n")


if __name__ == "__main__":
    asyncio.run(main())