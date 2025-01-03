import streamlit as st
import pandas as pd
import altair as alt
from modules.file_reader import process_uploaded_file
from modules.preprocessing import preprocess_text
from modules.ner import extract_named_entities_with_full_forms

st.title("Named Entity Recognition Tool")
st.write("Upload a PDF, Word, or TXT file to extract named entities after preprocessing.")

# File Upload
uploaded_file = st.file_uploader("Upload your file", type=["pdf", "docx", "txt"])

if uploaded_file:
    # Extract raw text from file
    raw_text = process_uploaded_file(uploaded_file)
    if raw_text:
        st.subheader("Raw Text")
        st.write(raw_text[:500])  # Display first 500 characters for preview
        
        # Preprocess text
        preprocessed_text = preprocess_text(raw_text)
        st.subheader("Preprocessed Text")
        st.write(preprocessed_text)
        
        # Extract Named Entities
        entities = extract_named_entities_with_full_forms(preprocessed_text)
        st.subheader("Named Entities Table")
        if entities:
            df = pd.DataFrame(entities, columns=["Entity", "Short Label", "Full Label"])
            df_sorted = df.sort_values(by=["Full Label", "Short Label"]).reset_index(drop=True)

             # Summary of Entity Counts
            st.subheader("Entity Type Summary")
            summary = df_sorted["Short Label"].value_counts().reset_index()
            summary.columns = ["Entity Type", "Count"]
            st.table(summary)

            # Visualization of Entity Counts
            st.subheader("Entity Type Distribution")
            chart = alt.Chart(summary).mark_bar().encode(
                x="Entity Type",
                y="Count",
                tooltip=["Entity Type", "Count"],
            ).properties(
                width=600,
                height=400
            )
            st.altair_chart(chart)

            # Filtering by Entity Types
            st.subheader("Filter Entities by Type")
            entity_types = df_sorted["Short Label"].unique()
            selected_types = st.multiselect(
                "Select Entity Types to Display",
                options=entity_types,
                default=entity_types
            )

            filtered_df = df_sorted[df_sorted["Short Label"].isin(selected_types)]
            st.table(filtered_df)  # Display filtered table

            csv = df_sorted.to_csv(index=False)
            st.download_button("Download NER Results as CSV", data=csv, file_name="ner_results.csv", mime="text/csv")

        else:
            st.write("No named entities found.")