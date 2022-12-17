import streamlit as st
from document_processing import document2text, preprocess_text, create_zip, create_csv
from widgets import displayPDF
import neuro


@st.cache(allow_output_mutation=True)
def load_model():
    model = neuro.init_model()
    return model


@st.cache(allow_output_mutation=True)
def load_tokenizer():
    tokenizer = neuro.init_tokenizer()
    return tokenizer


def make_prediction(model, tokenizer, file):
    original_text = document2text(file)
    text = preprocess_text(original_text)
    result = neuro.predict(model, tokenizer, text)
    return original_text, text, result


def visualize_file(file, original_text):
    st.subheader("Документ:")
    if file.name.endswith(".pdf"):
        displayPDF(file)
    else:
        # original text to unicode
        st.write("", original_text, disabled=True, height=1000)


def main():
    # load model and tokenizer
    model = load_model()
    tokenizer = load_tokenizer()

    st.title("Сервис для маршрутизации документов")
    st.write("Здесь вы можете загрузить документ и получить предсказание, куда его направить")
    files = st.file_uploader("Загрузите документ", type=["pdf", "docx", "doc", "rtf"], accept_multiple_files=True)
    if len(files) > 0:
        # make prediction
        predictions = [make_prediction(model, tokenizer, file) for file in files]

        # create table with file names and their predictions
        st.subheader("Результаты:")
        st.table(
            [{"Документ": file.name, "Предсказание": prediction[2]} for file, prediction in zip(files, predictions)])

        # create zip file with all files
        zip_file_name = create_zip(files, predictions)
        with open(zip_file_name, "rb") as f:
            zip_file = f.read()

        # click button and download .zip file
        st.download_button(
            label="Загрузить zip с отсортированными документами",
            data=zip_file,
            file_name='data.zip'
        )

        # click button and download .csv file
        csv_file = create_csv(files, predictions)
        st.download_button(
            label="Загрузить csv с предксказаниями",
            data=csv_file,
            file_name='predictions.csv'
        )

        # choose file to visualize
        file = st.selectbox("Выберите файл для просмотра", files, format_func=lambda x: x.name)
        original_text, text, result = make_prediction(model, tokenizer, file)
        visualize_file(file, original_text)


if __name__ == '__main__':
    main()
