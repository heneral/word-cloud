import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Try to import nltk for additional stopwords
try:
    import nltk
    from nltk.corpus import stopwords
    # Download if not present
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    nltk_stopwords = set(stopwords.words('english'))
except ImportError:
    nltk_stopwords = set()

# Combine stopwords
all_stopwords = STOPWORDS.union(nltk_stopwords)

# File to save responses
RESPONSES_FILE = "survey_responses.txt"

st.set_page_config(
    page_title="Survey Word Collector",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Survey Word Collector")
st.markdown("### Collect survey responses and generate word clouds")

# Custom CSS for form styling
st.markdown("""
<style>
/* .survey-form {
    background-color: #f8f9fa;
    padding: 25px;
    border-radius: 10px;
    border: 2px solid #3498db;
    margin-bottom: 20px;
} */
.response-input {
    margin-bottom: 15px;
}
.submit-button {
    background-color: #27ae60;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    font-weight: bold;
    width: 100%;
}
.success-message {
    background-color: #d4edda;
    color: #155724;
    padding: 15px;
    border-radius: 5px;
    border: 1px solid #c3e6cb;
    margin-top: 15px;
}
.wordcloud-section {
    background-color: #ecf0f1;
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["📝 Submit Response", "📊 View Responses", "☁️ Word Cloud"])

with tab1:
    st.markdown('<div class="survey-form">', unsafe_allow_html=True)
    st.markdown("### 📋 Survey Response Form")
    st.markdown("Please share your feedback or response:")

    # Response input
    response = st.text_area(
        "Your Response:",
        height=100,
        placeholder="Enter your survey response here...",
        help="Type your feedback, opinion, or response to the survey question."
    )

    # Optional: Add a question field
    question = st.text_input(
        "Question (optional):",
        placeholder="What question is this response for?",
        help="Specify the survey question if applicable"
    )

    # Submit button
    if st.button("💾 Save Response", key="submit", help="Save this response to the survey file"):
        if response.strip():
            # Prepare the entry
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = f"[{timestamp}]"

            if question.strip():
                entry += f" Question: {question.strip()}"

            entry += f"\nResponse: {response.strip()}\n{'-'*50}\n\n"

            # Save to file
            try:
                with open(RESPONSES_FILE, "a", encoding="utf-8") as f:
                    f.write(entry)

                st.markdown('<div class="success-message">', unsafe_allow_html=True)
                st.success("✅ Response saved successfully!")
                st.markdown(f"**Timestamp:** {timestamp}")
                if question.strip():
                    st.markdown(f"**Question:** {question.strip()}")
                st.markdown(f"**Response:** {response.strip()}")
                st.markdown('</div>', unsafe_allow_html=True)

                # Clear the form by rerunning
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error saving response: {str(e)}")
        else:
            st.warning("⚠️ Please enter a response before submitting.")

    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### 📊 View Collected Responses")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📂 View All Responses", help="Display all saved responses"):
            if os.path.exists(RESPONSES_FILE):
                try:
                    with open(RESPONSES_FILE, "r", encoding="utf-8") as f:
                        content = f.read()

                    if content.strip():
                        # Count responses
                        responses = content.split('-'*50)
                        response_count = len([r for r in responses if r.strip()])

                        st.info(f"📈 Total responses collected: {response_count}")

                        with st.expander("📝 View Responses", expanded=True):
                            st.text_area(
                                "Survey Responses:",
                                value=content,
                                height=300,
                                disabled=True
                            )
                    else:
                        st.info("📝 No responses collected yet.")
                except Exception as e:
                    st.error(f"❌ Error reading responses: {str(e)}")
            else:
                st.info("📝 No survey file exists yet. Submit your first response!")

    with col2:
        if st.button("📊 Response Statistics", help="Show basic statistics"):
            if os.path.exists(RESPONSES_FILE):
                try:
                    with open(RESPONSES_FILE, "r", encoding="utf-8") as f:
                        content = f.read()

                    if content.strip():
                        # Basic statistics
                        responses = content.split('-'*50)
                        valid_responses = [r for r in responses if r.strip()]

                        total_responses = len(valid_responses)
                        total_words = sum(len(r.split()) for r in valid_responses)
                        total_chars = sum(len(r) for r in valid_responses)

                        st.metric("Total Responses", total_responses)
                        st.metric("Total Words", total_words)
                        st.metric("Total Characters", total_chars)

                        # File size
                        file_size = os.path.getsize(RESPONSES_FILE)
                        st.metric("File Size", f"{file_size} bytes")
                    else:
                        st.info("📝 No responses to analyze yet.")
                except Exception as e:
                    st.error(f"❌ Error analyzing responses: {str(e)}")
            else:
                st.info("📝 No survey file exists yet.")

    # Download responses
    if os.path.exists(RESPONSES_FILE):
        with open(RESPONSES_FILE, "r", encoding="utf-8") as f:
            file_content = f.read()

        if file_content.strip():
            st.download_button(
                label="📥 Download Responses (.txt)",
                data=file_content,
                file_name="survey_responses.txt",
                mime="text/plain",
                help="Download all collected responses as a text file"
            )

with tab3:
    st.markdown("### ☁️ Generate Word Cloud")

    if os.path.exists(RESPONSES_FILE):
        try:
            with open(RESPONSES_FILE, "r", encoding="utf-8") as f:
                content = f.read()

            if content.strip():
                st.success("✅ Found survey responses! Ready to generate word cloud.")

                # Word cloud customization options
                col1, col2 = st.columns(2)

                with col1:
                    background_color = st.selectbox(
                        "Background Color:",
                        ["white", "black", "blue", "red", "green", "yellow", "purple"],
                        index=0,
                        help="Choose the background color for the word cloud"
                    )

                    colormap = st.selectbox(
                        "Color Scheme:",
                        ["viridis", "plasma", "inferno", "magma", "cividis", "cool", "hot", "rainbow"],
                        index=0,
                        help="Choose the color scheme for the words"
                    )

                    max_words = st.slider(
                        "Maximum Words:",
                        min_value=50,
                        max_value=500,
                        value=200,
                        step=25,
                        help="Maximum number of words to include in the cloud"
                    )

                with col2:
                    min_font_size = st.slider(
                        "Minimum Font Size:",
                        min_value=8,
                        max_value=20,
                        value=10,
                        step=1,
                        help="Minimum font size for words (affects smaller/frequent words)"
                    )

                    max_font_size = st.slider(
                        "Maximum Font Size:",
                        min_value=50,
                        max_value=200,
                        value=100,
                        step=10,
                        help="Maximum font size for words (affects larger/frequent words)"
                    )

                    relative_scaling = st.slider(
                        "Word Scaling:",
                        min_value=0.1,
                        max_value=1.0,
                        value=0.5,
                        step=0.1,
                        help="How much to scale words by frequency (higher = bigger difference between frequent and rare words)"
                    )

                # Generate word cloud button
                if st.button("🎨 Generate Word Cloud", help="Create a word cloud from all survey responses"):
                    with st.spinner("Generating word cloud..."):
                        try:
                            # Extract responses from the content
                            responses_text = ""
                            lines = content.split('\n')
                            for line in lines:
                                if line.startswith("Response:"):
                                    response = line.replace("Response:", "").strip()
                                    responses_text += response + " "

                            if responses_text.strip():
                                # Generate word cloud
                                wordcloud = WordCloud(
                                    width=800,
                                    height=400,
                                    background_color=background_color,
                                    colormap=colormap,
                                    max_words=max_words,
                                    stopwords=STOPWORDS,
                                    min_font_size=min_font_size,
                                    max_font_size=max_font_size,
                                    relative_scaling=relative_scaling,
                                    random_state=42
                                ).generate(responses_text)

                                # Create figure
                                fig, ax = plt.subplots(figsize=(10, 5))
                                ax.imshow(wordcloud, interpolation='bilinear')
                                ax.axis('off')
                                ax.set_title('Survey Responses Word Cloud', fontsize=16, pad=20)

                                # Display the word cloud
                                st.pyplot(fig)

                                # Save option
                                if st.button("💾 Save Word Cloud", help="Save the word cloud as an image file"):
                                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                    filename = f"wordcloud_{timestamp}.png"
                                    fig.savefig(filename, dpi=300, bbox_inches='tight')
                                    st.success(f"✅ Word cloud saved as '{filename}'")

                                    # Provide download link
                                    with open(filename, "rb") as f:
                                        st.download_button(
                                            label="📥 Download Word Cloud",
                                            data=f,
                                            file_name=filename,
                                            mime="image/png",
                                            help="Download the word cloud image"
                                        )
                            else:
                                st.warning("⚠️ No response text found to generate word cloud.")

                        except Exception as e:
                            st.error(f"❌ Error generating word cloud: {str(e)}")
            else:
                st.info("📝 No responses collected yet. Submit some responses first!")

        except Exception as e:
            st.error(f"❌ Error reading responses file: {str(e)}")
    else:
        st.info("📝 No survey responses file found. Submit some responses first!")

# Footer
st.markdown("---")
st.markdown("💡 **Survey Word Collector** - Collect responses and save to file for later analysis!")
st.markdown("*Perfect for survey data collection and research*")