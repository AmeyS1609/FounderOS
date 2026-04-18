"""Integration checks against a running FounderOS server (default localhost:8000)."""

from __future__ import annotations

import os
import traceback

import httpx

BASE = os.getenv("TEST_API_BASE", "http://127.0.0.1:8000")


def main() -> None:
    passed = 0
    failed: list[tuple[str, str]] = []

    def ok(name: str) -> None:
        nonlocal passed
        passed += 1
        print(f"{name}: PASS")

    def fail(name: str, err: str) -> None:
        failed.append((name, err))
        print(f"{name}: FAIL — {err}")

    with httpx.Client(base_url=BASE, timeout=300.0) as client:
        # 1 Health
        try:
            r = client.get("/")
            assert r.status_code == 200 and "status" in r.json(), r.text
            ok("Health check")
        except Exception as e:  # noqa: BLE001
            fail("Health check", f"{e}\n{traceback.format_exc()}")

        # 2 BI
        try:
            r = client.post(
                "/api/bi/analyze",
                json={"company": "Notion", "market": "productivity SaaS", "use_mock": True},
            )
            assert r.status_code == 200, r.text
            body = r.json()
            assert "analysis" in body and "swot" in body["analysis"], body
            pros = body["analysis"].get("pros") or []
            print("first pro:", pros[0] if pros else "<none>")
            ok("BI Agent")
        except Exception as e:  # noqa: BLE001
            fail("BI Agent", f"{e}\n{traceback.format_exc()}")

        # 3 Email auth
        try:
            r = client.get(
                "/api/email/inbox",
                headers={"Authorization": "Bearer FAKE_TOKEN_TEST"},
            )
            assert r.status_code == 401, r.text
            ok("Email auth")
        except Exception as e:  # noqa: BLE001
            fail("Email auth", f"{e}\n{traceback.format_exc()}")

        # 4 Leads webhook
        try:
            payload = {
                "transcript": (
                    "Agent: Hi I am Bhavpreet from FounderOS. What business are you building? "
                    "Caller: I am building a B2B SaaS for payroll automation. Just me and my co-founder right now. "
                    "Agent: How many hours per week do you spend on sales? "
                    "Caller: Honestly like 15 hours, it is killing me. I do all the cold outreach myself. "
                    "Agent: What would change if you had 5 warm leads per week without doing outreach? "
                    "Caller: That would completely change everything. I could actually focus on the product."
                ),
                "caller": {"name": "Test Lead"},
                "duration": 240,
            }
            r = client.post("/api/leads/webhook", json=payload)
            assert r.status_code == 200, r.text
            data = r.json()
            fs = int(data.get("fit_score", 0))
            assert 5 <= fs <= 10, data
            print("lead summary:", data.get("summary", ""))
            ok("Lead webhook")
        except Exception as e:  # noqa: BLE001
            fail("Lead webhook", f"{e}\n{traceback.format_exc()}")

        # 5 Talent
        try:
            r = client.post(
                "/api/talent/search",
                json={"role": "full-stack engineer", "location": "San Francisco", "experience_years": 2},
            )
            assert r.status_code == 200, r.text
            data = r.json()
            cands = data.get("candidates") or []
            assert isinstance(cands, list) and len(cands) >= 1, data
            first = cands[0]
            print("first candidate:", first.get("name"), first.get("fit_score"))
            ok("Talent search")
        except Exception as e:  # noqa: BLE001
            fail("Talent search", f"{e}\n{traceback.format_exc()}")

        # 6 CS easy
        try:
            r = client.post(
                "/api/csbot/message",
                json={"message": "How much does FounderOS cost?", "conversation_history": []},
            )
            assert r.status_code == 200, r.text
            d = r.json()
            assert d.get("confidence") == "high", d
            print("csbot reply:", d.get("reply", ""))
            ok("CS Bot easy")
        except Exception as e:  # noqa: BLE001
            fail("CS Bot easy", f"{e}\n{traceback.format_exc()}")

        # 7 CS hard
        try:
            r = client.post(
                "/api/csbot/message",
                json={
                    "message": "Can FounderOS integrate with SAP, Oracle, and Workday simultaneously with real-time bidirectional sync?",
                    "conversation_history": [],
                },
            )
            assert r.status_code == 200, r.text
            d = r.json()
            assert d.get("flagged_for_training") is True or d.get("confidence") == "low", d
            ok("CS Bot training flag")
        except Exception as e:  # noqa: BLE001
            fail("CS Bot training flag", f"{e}\n{traceback.format_exc()}")

        # 8 Training queue
        try:
            r = client.get("/api/csbot/training-queue")
            assert r.status_code == 200, r.text
            data = r.json()
            assert int(data.get("count", -1)) >= 0, data
            ok("Training queue")
        except Exception as e:  # noqa: BLE001
            fail("Training queue", f"{e}\n{traceback.format_exc()}")

    print()
    print(f"PASS count: {passed} / 8 tests passed")
    for name, err in failed:
        print(f"- {name}: {err}")


if __name__ == "__main__":
    main()
