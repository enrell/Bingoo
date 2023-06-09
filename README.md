# Bingoo
Basic Search Engine

Requirements:
- Node.js
- npm
- Python
- pip
- MySQL

Install the required Python libraries:
pip install requests beautifulsoup4 nltk mysql-connector-python

Setup:
1. Create the database and configure it in the indexer.py file. Look for the username and password setup in the file. The database file is located at db.sql in the project.

2. Navigate to the Bingoo/Bingoo directory:
<code>cd Bingoo/Bingoo</code>

3. Install the required Node.js dependencies:
<code>npm install</code>

4. Add your links to the indexer.py file.

5. Start the indexing process:
<code>python Indexer.py</code>

6. Start the development server:
7. <code>npm run dev</code>

7. Start the Node.js server:
<code>node server.js</code>

If you want to enable crawling, uncomment this line of code in the final Indexer.py file:
<code># crawl_links(links)</code>
