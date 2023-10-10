from httpx import AsyncClient


async def test_delete_task(tc: AsyncClient, user_lead, user_manager, new_task_id):
    response_wrong_role = await tc.delete(
        f"/tasks/{new_task_id}/delete", headers=user_lead
    )
    response_manager = await tc.delete(
        f"/tasks/{new_task_id}/delete", headers=user_manager
    )

    assert response_wrong_role.status_code == 403
    assert response_manager.status_code == 200


async def test_edit_task_status_flow(
    tc: AsyncClient, user_lead, user_dev, user_qa, new_task_id
):
    response_in_progress = await tc.patch(
        f"/tasks/{new_task_id}/status_asignee",
        json={"asignee": 3, "status": "In progress"},
        headers=user_lead,
    )
    response_in_review = await tc.patch(
        f"/tasks/{new_task_id}/status_asignee",
        json={"asignee": 2, "status": "Code review"},
        headers=user_dev,
    )
    response_dev_test = await tc.patch(
        f"/tasks/{new_task_id}/status_asignee",
        json={"asignee": 3, "status": "Dev test"},
        headers=user_lead,
    )
    response_test = await tc.patch(
        f"/tasks/{new_task_id}/status_asignee",
        json={"asignee": 4, "status": "Testing"},
        headers=user_dev,
    )
    response_done = await tc.patch(
        f"/tasks/{new_task_id}/status_asignee",
        json={"asignee": 4, "status": "Done"},
        headers=user_qa,
    )

    assert response_in_progress.status_code == 200
    assert response_in_review.status_code == 200
    assert response_dev_test.status_code == 200
    assert response_test.status_code == 200
    assert response_done.status_code == 200


async def test_edit_task_status_bug(
    tc: AsyncClient, user_lead, user_dev, user_qa, new_task_id
):
    response_in_progress = await tc.patch(
        f"/tasks/{new_task_id}/status_asignee",
        json={"asignee": 3, "status": "In progress"},
        headers=user_lead,
    )
    response_in_review = await tc.patch(
        f"/tasks/{new_task_id}/status_asignee",
        json={"asignee": 2, "status": "Code review"},
        headers=user_dev,
    )
    response_dev_test = await tc.patch(
        f"/tasks/{new_task_id}/status_asignee",
        json={"asignee": 3, "status": "Dev test"},
        headers=user_lead,
    )
    response_test = await tc.patch(
        f"/tasks/{new_task_id}/status_asignee",
        json={"asignee": 4, "status": "Testing"},
        headers=user_dev,
    )
    response_bug = await tc.patch(
        f"/tasks/{new_task_id}/status_asignee",
        json={"asignee": 3, "status": "In progress"},
        headers=user_qa,
    )
    response_bug_review = await tc.patch(
        f"/tasks/{new_task_id}/status_asignee",
        json={"asignee": 2, "status": "Code review"},
        headers=user_dev,
    )
    response_bug_dev_test = await tc.patch(
        f"/tasks/{new_task_id}/status_asignee",
        json={"asignee": 3, "status": "Dev test"},
        headers=user_dev,
    )
    response_bug_test = await tc.patch(
        f"/tasks/{new_task_id}/status_asignee",
        json={"asignee": 4, "status": "Testing"},
        headers=user_dev,
    )
    response_done = await tc.patch(
        f"/tasks/{new_task_id}/status_asignee",
        json={"asignee": 4, "status": "Done"},
        headers=user_qa,
    )

    assert response_in_progress.status_code == 200
    assert response_in_review.status_code == 200
    assert response_dev_test.status_code == 200
    assert response_test.status_code == 200
    assert response_bug.status_code == 200
    assert response_bug_review.status_code == 200
    assert response_bug_dev_test.status_code == 200
    assert response_bug_test.status_code == 200
    assert response_done.status_code == 200
