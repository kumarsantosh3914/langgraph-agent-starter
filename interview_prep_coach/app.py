import uuid
import gradio as gr
from dotenv import load_dotenv

load_dotenv(override=True)

# pyrefly: ignore [missing-import]
from graph import graph

thread_id = str(uuid.uuid4())

async def process_message(message, success_criteria, history, thread):
    config = {"configurable": {"thread_id": thread}}
    state = {
        "messages": [{"role": "user", "content": message}],
        "success_criteria": success_criteria or "Provide well-researched, tailored interview questions and helpful feedback",
        "feedback_on_work": None,
        "success_criteria_met": False,
        "user_input_needed": False,
    }
    result = await graph.ainvoke(state, config=config)
    user = {"role": "user", "content": message}
    reply = {"role": "assistant", "content": result["messages"][-2].content}
    feedback = {"role": "assistant", "content": result["messages"][-1].content}
    return history + [user, reply, feedback]

async def reset():
    return "", "", None, str(uuid.uuid4())

with gr.Blocks(theme=gr.themes.Default(primary_hue="blue")) as demo:
    gr.Markdown("## Interview Prep Coach 🤖")
    thread = gr.State(thread_id)

    chatbot = gr.Chatbot(label="Coach", height=400)
    with gr.Group():
        message = gr.Textbox(
            show_label=False,
            placeholder="e.g. I'm interviewing for a backend engineer role at Stripe",
        )
        success_criteria = gr.Textbox(
            show_label=False,
            placeholder="Success criteria (optional)",
        )
    with gr.Row():
        reset_button = gr.Button("Reset", variant="stop")
        go_button = gr.Button("Go!", variant="primary")
 
    message.submit(process_message, [message, success_criteria, chatbot, thread], [chatbot])
    go_button.click(process_message, [message, success_criteria, chatbot, thread], [chatbot])
    reset_button.click(reset, [], [message, success_criteria, chatbot, thread])

if __name__ == "__main__":
    demo.launch()