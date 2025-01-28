<!-- @format -->

# AI Challenge - Unfamiliar Code Challenge

## Welcome! 👋

This challenge is brought to you by the Endava AI Champions.

## Requirements

- Solid Python knowledge
- License for GitHub Copilot

IMPORTANT: Check the [Artifacts](#expected-artifacts) before start.

## Goal

The goal of this challenge is to explore the capabilities of GitHub Copilot in assisting developers to resolve an open issue within an existing codebase. The focus will be on a closed issue from the FastAPI open-source project, where your task is to implement a fix for the identified problem.

## Constraints

- Avoid using web searches or official documentation as primary resources.
- Rely on GitHub Copilot for guidance, code generation, and best practices throughout the process.
- Upload your progress periodically by committing and pushing your changes to your branch. This ensures your work is backed up, accessible, and allows for smoother collaboration and support during the challenge.

## The challenge

Participants will access to the attached fastapi folder and explore the codebase to understand its structure and functionality. They will then work on resolving the specified issue with the assistance of GitHub Copilot. In addition to creating the PR, participants must provide a comprehensive explanation of how GitHub Copilot was utilized throughout the process.

## Issue

🐛 Fix JSON Schema accepting bools as valid JSON Schemas, e.g. additionalProperties: false

A "valid JSON Schema" includes a bool (i.e. true and false).

additionalProperties doesn't have to be a JSON object, it can be false, to mean no additional properties are allowed.

When I upgraded the JSON Schema models to include the new types and fields for the new JSON Schema 2020-12 I removed bool as a valid JSON Schema.

I reviewed all the spec again, this updates all the other fields that would allow bool as a valid value.

### Example code

```python
from fastapi import FastAPI
from pydantic import BaseModel
import json
import sys

class FooBaseModel(BaseModel):
    class Config:
        extra = "forbid"

class Foo(FooBaseModel):
    pass

app = FastAPI()

@app.post("/")
async def post(
    foo: Foo = None,
):
    pass

if __name__ == "__main__":
    oapi = app.openapi()
    json.dump(oapi, sys.stdout, indent=2)
```

### Description

Upgrading from FastAPI 0.98.0 to 0.99.0 causes OpenAPI failures. The error message looks similar to some previous issues (#3782, #383) but I'm unclear whether the issue is the same or different. In both cases, I'm running Pydantic 1.10.10.

On FastAPI 0.98.0, I get the following output when running the above script:

```python
$ pip install fastapi==0.98.0
Requirement already satisfied: fastapi==0.98.0 in /opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages (0.98.0)
Requirement already satisfied: pydantic!=1.8,!=1.8.1,<2.0.0,>=1.7.4 in /opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages (from fastapi==0.98.0) (1.10.10)
Requirement already satisfied: starlette<0.28.0,>=0.27.0 in /opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages (from fastapi==0.98.0) (0.27.0)
Requirement already satisfied: typing-extensions>=4.2.0 in /opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages (from pydantic!=1.8,!=1.8.1,<2.0.0,>=1.7.4->fastapi==0.98.0) (4.7.0)
Requirement already satisfied: anyio<5,>=3.4.0 in /opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages (from starlette<0.28.0,>=0.27.0->fastapi==0.98.0) (3.7.0)
Requirement already satisfied: idna>=2.8 in /opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages (from anyio<5,>=3.4.0->starlette<0.28.0,>=0.27.0->fastapi==0.98.0) (3.4)
Requirement already satisfied: sniffio>=1.1 in /opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages (from anyio<5,>=3.4.0->starlette<0.28.0,>=0.27.0->fastapi==0.98.0) (1.3.0)
Requirement already satisfied: exceptiongroup in /opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages (from anyio<5,>=3.4.0->starlette<0.28.0,>=0.27.0->fastapi==0.98.0) (1.1.1)

$ python repro.py
{
  "openapi": "3.0.2",
  "info": {
    "title": "FastAPI",
    "version": "0.1.0"
  },
  "paths": {
    "/": {
      "post": {
        "summary": "Post",
        "operationId": "post__post",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/Foo"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "Foo": {
        "title": "Foo",
        "type": "object",
        "properties": {},
        "additionalProperties": false
      },
      "HTTPValidationError": {
        "title": "HTTPValidationError",
        "type": "object",
        "properties": {
          "detail": {
            "title": "Detail",
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/ValidationError"
            }
          }
        }
      },
      "ValidationError": {
        "title": "ValidationError",
        "required": [
          "loc",
          "msg",
          "type"
        ],
        "type": "object",
        "properties": {
          "loc": {
            "title": "Location",
            "type": "array",
            "items": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "integer"
                }
              ]
            }
          },
          "msg": {
            "title": "Message",
            "type": "string"
          },
          "type": {
            "title": "Error Type",
            "type": "string"
          }
        }
      }
    }
  }
}
```

After upgrading to FastAPI 0.99.0, using the same version of Pydantic, I get schema validation failures instead:

```python
$ pip install fastapi==0.99.0
Requirement already satisfied: fastapi==0.99.0 in /opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages (0.99.0)
Requirement already satisfied: pydantic!=1.8,!=1.8.1,<2.0.0,>=1.7.4 in /opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages (from fastapi==0.99.0) (1.10.10)
Requirement already satisfied: starlette<0.28.0,>=0.27.0 in /opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages (from fastapi==0.99.0) (0.27.0)
Requirement already satisfied: typing-extensions>=4.5.0 in /opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages (from fastapi==0.99.0) (4.7.0)
Requirement already satisfied: anyio<5,>=3.4.0 in /opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages (from starlette<0.28.0,>=0.27.0->fastapi==0.99.0) (3.7.0)
Requirement already satisfied: idna>=2.8 in /opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages (from anyio<5,>=3.4.0->starlette<0.28.0,>=0.27.0->fastapi==0.99.0) (3.4)
Requirement already satisfied: sniffio>=1.1 in /opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages (from anyio<5,>=3.4.0->starlette<0.28.0,>=0.27.0->fastapi==0.99.0) (1.3.0)
Requirement already satisfied: exceptiongroup in /opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages (from anyio<5,>=3.4.0->starlette<0.28.0,>=0.27.0->fastapi==0.99.0) (1.1.1)

$ python repro.py
Traceback (most recent call last):
  File "/Users/jawnsy/projects/work/prefect/repro.py", line 22, in <module>
    oapi = app.openapi()
  File "/opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages/fastapi/applications.py", line 218, in openapi
    self.openapi_schema = get_openapi(
  File "/opt/homebrew/Caskroom/miniconda/base/envs/prefect2-dev/lib/python3.10/site-packages/fastapi/openapi/utils.py", line 466, in get_openapi
    return jsonable_encoder(OpenAPI(**output), by_alias=True, exclude_none=True)  # type: ignore
  File "pydantic/main.py", line 341, in pydantic.main.BaseModel.__init__
pydantic.error_wrappers.ValidationError: 2 validation errors for OpenAPI
components -> schemas -> Foo -> additionalProperties
  value is not a valid dict (type=type_error.dict)
components -> schemas -> Foo -> $ref
  field required (type=value_error.missing)
```

## What are you going to practice?

- Leveraging GitHub Copilot as a collaborative tool in bug analysis.

## Building the Challenge - Instructions

Before You Begin:

1. Download the Repository: Start by downloading the current repository to your local machine.
2. Create a Branch: Create a new branch using your name as the pattern: {your-name} (e.g., edward-montoya).
3. Verify GitHub Copilot Configuration: Ensure that GitHub Copilot for Enterprise is properly configured in Visual Studio Code.
4. Set Up Your Repository: Configure your repository so that your code is published to your branch. This setup will also be beneficial if you need assistance during the challenge, as you can share the URL for your project/branch with your repository URL. There are various methods to achieve this.

Suggested Process:
While the following steps are recommended, feel free to approach the challenge in your own way:

1. Explore the Issue: Review the details of Issue to understand the problem and the context in which it occurs.
2. Utilize GitHub Copilot: Use GitHub Copilot to assist in understanding the code, identifying potential solutions, and writing code to resolve the issue.
3. Implement the Solution: Write the necessary code to fix the issue, ensuring that the solution is integrated well with the existing codebase.
4. Test the Solution: Ensure that the solution is thoroughly tested and does not introduce new bugs. A NEW test case MUST be created.
5. Document the Process: Participants should document how GitHub Copilot assisted them in solving the issue, including any challenges faced and how they were overcome.

## Expected Artifacts

The final deliverable for this challenge should be a Pull Request (PR) submitted to the repository. This PR should include all the code and resources completed during the challenge. It will serve as the primary artifact for reviewing and assessing your work.

> The PR must also include your insights on using GitHub Copilot during the exercise, following the schema below:

```
## Pull Request Title

## Description
- **Technology Used:** Describe the tools, frameworks, or languages you utilized.
- **What I Learned:** Summarize key takeaways or skills acquired during the challenge.
- **Useful Resources:** List any references, articles, or documentation that were helpful.

## Testing
- **Testing Approach:** Outline the strategy used for testing the challenge.
- **Test Methods:** Include details on any unit tests, integration tests, or manual testing performed.

## Visual Evidence
- **GitHub Copilot Interactions:** Attach relevant screenshots, screen recordings, or GIFs that highlight valuable interactions with GitHub Copilot.

## Checklist
- [ ] I have documented relevant GitHub Copilot scenarios (if applicable).
- [ ] The challenge is fully completed.

## Additional Comments
- **Further Insights:** Provide any additional information or notes, such as potential risks, edge cases, or alternative approaches considered.
```

## Feedback on GitHub Copilot

Please include the following in your PR:

- Strengths: How did Copilot help during the challenge?
- Limitations: Where did it struggle?
- Suggestions: How could Copilot improve for SQL optimization?
- Prompt: Revelant/Useful prompts
- Strategies: Approaches to solve the challenge

## Got feedback for us?

We love receiving feedback! We're always looking to improve our process. So if you have anything you'd like to mention, please email us.

**Have fun building!** 🚀
