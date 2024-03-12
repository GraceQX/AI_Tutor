from openai import OpenAI
import time


def send_query_get_response(client, user_question, assistant_id, in_lecture_mode=False):
    # Create a new thread for the query
    thread = client.beta.threads.create()
    thread_id = thread.id

    # user_question=user_question+ ' and tell me which file are the top results based on your similarity search'
    user_question = user_question + (' In Lecture mode: ' if in_lecture_mode else '')  # 根据 in_lecture_mode 添加回答用词

    # Send the user's question to the thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_question,
    )

    # Create and start a run for the thread
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    # Initialize a timer to limit the response wait time
    start_time = time.time()

    # Continuously check the run status
    run_status = None
    while run_status != 'completed':
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        run_status = run.status

        # Time check to break the loop if it runs more than 60 seconds
        if time.time() - start_time > 60:
            print("Final run status:", run_status)
            print("Took too long time")
            break

    # Fetch and print the entire conversation history
    messages = client.beta.threads.messages.list(
        thread_id=thread_id,
        order='asc'
    )

    # Return the last response from the thread
    message=messages.data[-1]
    message_content=message.content[0].text
    response=message_content.value

    return response if messages.data else "Server issue, try again"



