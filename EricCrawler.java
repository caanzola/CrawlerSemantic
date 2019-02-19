import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;

public class EricCrawler {

	private HashSet<String> links;
	private HashSet<String> papersLinks;
	private ArrayList<String> papers;
	private static final int MAX_DEPTH = 4;   
	private boolean go = true;
	private boolean goNonJournal = true;

	public EricCrawler(){
		links = new HashSet<String>();
		papersLinks = new HashSet<String>();
		papers = new ArrayList<String>();
	}

	public void getPageLinks(String URL, int depth) {
		if((URL.contains("q=source") || go) && !URL.contains("thesaurus") && !URL.contains("collection")) {
			go = false;
			Long initialTime = System.currentTimeMillis();
			//4. Check if you have already crawled the URLs 
			//(we are intentionally not checking for duplicate content in this example)
			if ((!links.contains(URL) && (depth <  MAX_DEPTH))) {
				System.out.println(">> Depth: " + depth + " [" + URL + "]");
				try {
					//4. (i) If not add it to the index
					if (links.add(URL)) {
						System.out.println(URL);
					}
					if(depth == 3 && papersLinks.add(URL)) {

					}

					Long checkTime = System.currentTimeMillis();
					while(checkTime - initialTime < 250) {
						checkTime = System.currentTimeMillis();
					}
					//2. Fetch the HTML code
					Document document = Jsoup.connect(URL).get();
					//3. Parse the HTML to extract links to other URLs
					Elements linksOnPage;
					if(depth == 0) {
						linksOnPage = document.select("a[href]");
					}
					else if(depth == 1) {
						linksOnPage = document.select("a[href*=\"&pg=\"]");
					}
					else if(depth == 2) {
						linksOnPage = document.select("a[href*=\"id=EJ\"]");
					}
					else {
						linksOnPage = document.select("a[href^=\"http://eric.ed.gov/\"]");
					}
					depth++;
					//5. For each extracted URL... go back to Step 4.
					for (Element page : linksOnPage) {
						if(links.size() == 20000) break;
						getPageLinks(page.attr("abs:href"), depth);
					}
				} catch (IOException e) {	
					System.err.println("For '" + URL + "': " + e.getMessage());
				}
			}
		}

	}

	public void	getPageLinksNonJournal(String URL, int depth) {
		if( (goNonJournal || URL.contains("q=source") ) && !URL.contains("thesaurus") && !URL.contains("collection")) {
			goNonJournal = false;
			Long initialTime = System.currentTimeMillis();
			//4. Check if you have already crawled the URLs 
			//(we are intentionally not checking for duplicate content in this example)
			if ((!links.contains(URL) && (depth <  MAX_DEPTH))) {
				System.out.println(">> Depth: " + depth + " [" + URL + "]");
				try {
					//4. (i) If not add it to the index
					if (links.add(URL)) {
						System.out.println(URL);
					}
					if(depth == 3 && papersLinks.add(URL)) {

					}

					Long checkTime = System.currentTimeMillis();
					while(checkTime - initialTime < 250) {
						checkTime = System.currentTimeMillis();

					}
					//2. Fetch the HTML code
					Document document = Jsoup.connect(URL).get();
					//3. Parse the HTML to extract links to other URLs
					Elements linksOnPage;
					if(depth == 0) {
						linksOnPage = document.select("a[href]");
					}
					else if(depth == 1) {
						linksOnPage = document.select("a[href*=\"&pg=\"]");
					}
					else if(depth == 2) {
						linksOnPage = document.select("a[href*=\"id=ED\"]");
					}
					else {
						linksOnPage = document.select("a[href^=\"http://eric.ed.gov/\"]");
					}
					depth++;
					//5. For each extracted URL... go back to Step 4.
					for (Element page : linksOnPage) {
						if(links.size() == 40000) break;
						getPageLinksNonJournal(page.attr("abs:href"), depth);
					}
				} catch (IOException e) {	
					System.err.println("For '" + URL + "': " + e.getMessage());
				}
			}
		}

	}
	public void getInfo() {
		papersLinks.forEach(x -> {
			Document document;
			try {
				//String para ir agregando las tuplas 
				String addInfo = "";

				document = Jsoup.connect(x).get();
				String title = document.select("div[class=\"title\"]").text();
				String author = document.getElementsByClass("r_a").first().child(0).text();
				String source = document.select("cite").text();

				Element container = document.select("div[id=\"r_colR\"]").select("div[style*=\"padding-left:\"]").first();
				String recordType = container.child(1).text();
				String date = container.child(2).text(); 

				addInfo = title + '*' + author + '*' + date + '*' + source + '*' + recordType;
				papers.add(addInfo);System.out.println(addInfo);
			} catch (IOException e) {
				System.err.println(e.getMessage());
			}
		});
	}

	public int BiggestNumAuthors() {
		int max = 0;
		for(String paper : papers) {
			String[] sep = paper.split("\\*");
			String autores = sep[1];
			String[] cadaAutor = autores.split(";");
			if(cadaAutor.length > max)
				max = cadaAutor.length;
		}
		return max;
	}

	public void writeCSV() {
		FileWriter writer = null;
		try {
			writer  = new FileWriter(new File("eric.csv"));
			String header = "title,";
			int maxAuthors = BiggestNumAuthors();
			for(int i = 0; i < maxAuthors; i++ ) {
				header += "author" + i + ",";
			}
			header += "date,source,recordType\n";
			writer.append(header);


			for(String paper : papers) {
				String[] sep = paper.split("\\*");
				writer.append(sep[0]);
				writer.append(',');
				String[] cadaAutor = sep[1].split(";");
				for( int j = 0; j < maxAuthors; j++) {
					if(j >= cadaAutor.length) {
						writer.append("");
						writer.append(',');
					}
					else {
						String[] autor = cadaAutor[j].split(",");
						if(autor.length != 2) writer.append(autor[0]);
						else writer.append(autor[1] + " " + autor[0]);
						writer.append(',');
					}
				}
				writer.append(sep[2].split(":")[1]);
				writer.append(',');
				writer.append(sep[3]);
				writer.append(',');
				writer.append(sep[4].split(":")[1]);
				writer.append('\n');
			}

		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		finally {

			try {
				writer.flush();
				writer.close();
			} catch (IOException e) {
				System.out.println("Error while flushing/closing fileWriter !!!");
				e.printStackTrace();
			}

		}
	}

	public static void main(String[] args) {
		//1. Pick a URL from the frontier
		EricCrawler crawler = new EricCrawler();
		crawler.getPageLinks("https://eric.ed.gov/?journals",0);
		crawler.getPageLinksNonJournal("https://eric.ed.gov/?nonjournals", 0);
		crawler.getInfo();
		crawler.writeCSV();
	}

}