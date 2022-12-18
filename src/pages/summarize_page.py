import streamlit as st
from src.processings.document_processing import create_txt
from src import neuro


def main():
    st.title("Резюмирование текста")
    st.write("Здесь вы можете загрузить документ и получить сокращённый текст")
    file = st.file_uploader("Загрузите документ", type=["pdf", "docx", "doc", "rtf"], accept_multiple_files=False)
    if file is not None:
        # slider to choose sentence number
        sentence_number = st.slider("Выберите размер желаемого текста:", 1, 10, 0)
        text = neuro.summarize_file(file, sentence_number=sentence_number)
        st.write('Обработка запроса...')
        st.subheader("Сокращенный текст:")
        st.write(text)

        # create .txt file with new text
        file = create_txt(text)
        st.download_button(
            label="Загрузить txt с сокращённым текстом",
            data=file,
            file_name='short_doc.txt'
        )


if __name__ == '__main__':
    main()
