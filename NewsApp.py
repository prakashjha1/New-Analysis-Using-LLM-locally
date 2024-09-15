import streamlit as st
from GoogleNews import GoogleNews
from Agent import summarizer,interpreter,Task,Crew,planner
class NewsFetcher:
    def __init__(self, topic, max_results, period):
        self.topic = topic
        self.max_results = max_results
        self.period = period
        self.news_client = GoogleNews(period=self.period)

    def fetch_news(self):
        self.news_client.search(self.topic)
        results = []
        current_page = 1

        while len(results) < self.max_results:
            new_results = self.news_client.page_at(current_page)
            if not new_results:
                break
            results.extend(new_results)
            current_page += 1

        return results[:self.max_results]

class NewsApp:
    def __init__(self):
        st.title("News Analysis App")
        self.topic = st.text_input("Enter news topic:", "")
        self.max_results = st.number_input("Enter maximum number of results:", min_value=1, max_value=100, value=10)
        self.period = st.selectbox("Select period:", ['1d', '2d','3d','4d','5d','7d', '1m', '1y'])
        self.news_fetcher = None

    def run(self):
        if st.button("Fetch News"):
            if self.topic:
                self.news_fetcher = NewsFetcher(self.topic, self.max_results, self.period)
                news = self.news_fetcher.fetch_news()
                self.display_layout(news)
            else:
                st.error("Please enter a topic to fetch news.")

    def display_layout(self, news):
        col1, col2 = st.columns(2)

        with col1:
            self.display_news(news)
        
        with col2:
            self.display_analysis(news)

    def display_news(self, news):
        st.subheader("News Articles")
        for article in news:
            st.markdown(f"**{article['title']}**")
            st.write(article['desc'])
            st.write(f"Published on: {article['date']}")
            st.write(f"[Read more]({article['link']})")
            st.write("")

    def display_analysis(self, news):
        st.subheader("Overall Analysis")
        analysis = self.analyze_news(news)
        st.write(analysis)

    def analyze_news(self, news_list):
        
        
        data = ''
        for news in news_list: 
            data += f"\n{news['title']}\n description:{news['desc']}"
        
        
        summarizing_task = Task(
            description=f"Summarize the following data: {data}",
            agent=summarizer
        )

        interpreting_task = Task(
            description="Interpret the summarized data and provide insights.",
            agent=interpreter
        )

        planning_task = Task(
            description="Create an actionable plan based on the summarized and interpreted data for Trading in Stock Market. I am interested in Buy or sell signal (Opportunities) from the provided information",
            agent=planner
        )

        # Create the crew
        crew = Crew(
            agents=[summarizer, interpreter, planner],
            tasks=[summarizing_task, interpreting_task, planning_task]
        )

        # Start the crew's work
        result = crew.kickoff()
        
        
        return result

if __name__ == "__main__":
    app = NewsApp()
    app.run()
