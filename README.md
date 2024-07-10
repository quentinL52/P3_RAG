# P3_RAG
 **RAG system for job recommandation based on CV**

this project use a pdf loader to take a cv, then the cv will be embedded through huggin face sentence transformers.
the cv will then be indexed in pinecone vectorstore, on a specific CV index (using 768 dimension vectors).
on the other hand a data base of job offer have been collected and embedded on another index (still 768 dimensions)
for the recommandation part the model will use 2 retrievers, one for the CV and another for the job offers database, the model will then calculate the similarity and return adapted offer according to the caracteristics on the curriculum.

for this project the main goal was DATA oriented jobs.

the  API used :
- i used the free tiers pinecone vector store.
- groq API for the llama3 70b model.
