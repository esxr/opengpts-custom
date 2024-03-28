export const TYPES = {
  agent: {
    id: "agent",
    title: "Assistant",
    description:
      "Steps to create a custom bot for a company: \n1. Load the pdf file in the the 'Files' section below. \n2. Select your custom API that you added from the dropdown. \n3. Give the initial instructions. Don't forget to tell the bot to look up the API where necessary. \n4. Save the bot!",
    files: true,
  },
  chatbot: {
    id: "chatbot",
    title: "Chatbot",
    description:
      "These GPTs are solely parameterized by arbitrary instructions. This makes them great at taking on specific personas or characters. Because these are a relatively simple architecture, these work well with even less powerful models.",
    files: false,
  },
  chat_retrieval: {
    id: "chat_retrieval",
    title: "RAG",
    description:
      "These GPTs can be given an arbitrary number of files, and you can give them arbitrary instructions. During each interaction the files are searched once (and only once) for relevant information, and then GPT responds to the user. This makes them perfect if you want to create a simple GPT that has knowledge of external data. Because these are a relatively simple architecture, these work well with even less powerful models.",
    files: true,
  },
} as const;

export type TYPE_NAME = (typeof TYPES)[keyof typeof TYPES]["id"];

export const DROPZONE_CONFIG = {
  multiple: true,
  accept: {
    "text/*": [".txt", ".htm", ".html"],
    "application/pdf": [".pdf"],
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [
      ".docx",
    ],
    "application/msword": [".doc"],
  },
  maxSize: 10_000_000, // Up to 10 MB file size.
};
