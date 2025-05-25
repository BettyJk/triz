import streamlit as st
import json
import os
from groq import Groq
from difflib import get_close_matches

# Load TRIZ data
with open('trizprincipals.json') as f:
    triz_principles = {int(k): v for item in json.load(f)['TRIZ_40_Principles'] for k, v in item.items()}

with open('trizmatrixx.json') as f:
    contradiction_matrix = json.load(f)

# Initialize Groq client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Failed to initialize Groq client: {str(e)}")
    st.stop()

def identify_parameters(user_input):
    prompt = f"""Analyze this engineering problem and identify ONLY the single most relevant parameter to improve 
    from this exact list: {', '.join({m['improving'] for m in contradiction_matrix})}

    Return JUST ONE parameter name from the list above. Example: \"Strength\"

    Problem: {user_input}"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.1,
            max_tokens=50
        )
        raw_response = chat_completion.choices[0].message.content

        improving = None
        for param in {m['improving'] for m in contradiction_matrix}:
            if param.lower() in raw_response.lower():
                improving = param
                break

        if not improving:
            st.warning("AI response didn't match known parameters. Using fallback...")
            improving = manual_parameter_identification(raw_response, [m['improving'] for m in contradiction_matrix])

        return improving, "Weight of moving object"

    except Exception as e:
        st.warning(f"AI analysis failed: {str(e)}. Using manual fallback...")
        return manual_parameter_identification(user_input, [m['improving'] for m in contradiction_matrix]), "Weight of moving object"

def manual_parameter_identification(user_input, parameters):
    matches = get_close_matches(user_input.lower(), [p.lower() for p in parameters], n=1)
    return matches[0].capitalize() if matches else None

def generate_real_life_solution(problem, principle_num, industry="general"):
    prompt = f"""
You are an expert TRIZ engineer.

Given the following engineering problem:
\"{problem}\"

And TRIZ Principle {principle_num}: \"{triz_principles.get(principle_num, 'Unknown')}\",

Generate 1-2 real-life solution examples or strategies that apply this principle to solve the problem — especially for the \"{industry}\" industry. Be specific and realistic (e.g., techniques, materials, configurations used in known products or systems).

Format:
•⁠  ⁠Real-life Solution 1: ...
•⁠  ⁠Real-life Solution 2: ...
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.5,
            max_tokens=5096
        )
        
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        st.warning(f"AI failed to generate solution: {str(e)}")
        return "Could not generate solution due to API error."
#ddddd
def evaluate_solution(solution_text, attributes, industry, problem):
    prompt = f"""
Given this engineering problem: "{problem}"
And the proposed solution: \"\"\"{solution_text}\"\"\"

Evaluate it on the following criteria from 0 to 10, based on its relevance to the {industry} industry:
{json.dumps(attributes, indent=2)}

Return the results in the format:
Feasibility: X/10 - [reason]
Cost-Efficiency: X/10 - [reason]
Originality: X/10 - [reason]
Industry Fit: X/10 - [reason]
"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.3,
            max_tokens=1024
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        st.warning(f"AI evaluation failed: {str(e)}")
        return "Evaluation failed."
#fffffff

st.set_page_config(page_title="TRIZ Problem Solver", page_icon="⚙️", layout="wide")
#ddddddddddddddd
st.sidebar.header("📊 Evaluation Priorities")

attributes = {
    "Feasibility": st.sidebar.slider("Feasibility", 0, 10, 5),
    "Cost-Efficiency": st.sidebar.slider("Cost-Efficiency", 0, 10, 5),
    "Originality": st.sidebar.slider("Originality", 0, 10, 5),
    "Industry Fit": st.sidebar.slider("Industry Fit", 0, 10, 5)
}
#fffffffffffff
st.title(" TRIZ Engineering Problem Solver")
st.markdown("### Your problem-solving assistant for engineering contradictions")

with st.expander(" How it works"):
    st.markdown("""
    1. Describe your engineering problem with contradictory requirements  
    2. AI identifies the key parameter to improve  
    3. System matches against TRIZ contradiction matrix  
    4. Recommends innovation principles with *real-world solutions*  
    """)
industry = st.selectbox(
    "Select the target industry:",
    ["general", "automotive", "aerospace", "medical", "electronics", "manufacturing"]
)

problem = st.text_area("Describe your engineering problem:", height=150,
                       placeholder="e.g., 'We need stronger body panels but they're making the vehicle too heavy'")

if st.button("Solve Problem"):
    if not problem.strip():
        st.warning("Please describe your engineering problem")
        st.stop()

    with st.spinner(" Analyzing problem..."):
        improving, worsening = identify_parameters(problem)

    if improving:
        st.success(f"Identified contradiction: Improving *{improving}* vs Worsening *{worsening}*")

        solution = next((item for item in contradiction_matrix if item['improving'] == improving), None)

        if solution:
            principles = solution['principles']
            st.subheader(" TRIZ Principles with Real-Life Solutions & Rationale")
            all_solutions = []
            for principle_num in principles[:6]:
                principle_name = triz_principles.get(principle_num, 'Unknown')
                ai_solution = generate_real_life_solution(problem, principle_num, industry)
                

                st.markdown(f"### Principle {principle_num}: {principle_name}")
                st.markdown(f"* Real-life Solutions:*\n{ai_solution}")
                evaluation = evaluate_solution(ai_solution, attributes, industry, problem)
                st.markdown(f" **Evaluation Metrics**\n{evaluation}")


                all_solutions.append({
                    "principle_num": principle_num,
                    "name": principle_name,
                    "solution": ai_solution
                })

            st.subheader("🏆 Optimal Recommendation")

            best_prompt = f"""
We have the following TRIZ principle applications for the problem:

Problem: \"{problem}\"
Industry: {industry}

Principle Options:
{json.dumps([{k: v for k, v in p.items() if k in ['principle_num', 'name', 'benefit']} for p in all_solutions], indent=2)}

Based on the problem and industry context, which principle is *most effective* and *why*?
Explain the logic clearly, referencing both benefits and practical applicability.
"""

            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": best_prompt}],
                    model="llama3-8b-8192",
                    temperature=0.3,
                    max_tokens=4096
                )
                optimal_analysis = chat_completion.choices[0].message.content.strip()
                st.info(optimal_analysis)
            except Exception as e:
                st.warning(f"AI couldn't generate optimal explanation: {str(e)}")

        else:
            st.warning("No direct principles found. Applying separation strategies...")
            st.markdown("""
            *Try these approaches:*
            1. Separate in Time (e.g., temporary structures)  
            2. Separate in Space (e.g., distributed systems)  
            3. Change Scale (e.g., nano-materials)  
            4. Transition to Supersystem (e.g., shared components)
            """)

    st.markdown("---")
    st.caption("TRIZ Problem Solver v2.0 | created by Bouthayna Jouak and Hajar EL Hadri | Powered by Llama3")