1.) Please install the required python libraries specified in requirements.txt (pip install -r requirements.txt).

2.) If error is encountered when installing the required dependencies, please use do the following: pip install beautifulsoup and pip install pandas.

3.) Please read blog for how the program works - https://www.ishareinfo.com/post/alternative-mitre-att-ck-navigator-my-mitre-att-ck-visualizer-2-0 or read the html file in the repository.

4.) The main program to run is Mitre_Attack_Enterprise_Matrix_Visualisation (Main).py which will call functions from the rest of the python files in the code repository.

5.) The program includes a function that retrieves threat actor group(s), as tracked by MITRE, from a default text file (threat_actor_group.txt). 

6.) The program will use the frequency count to apply a color gradient to each cell in the matrix. The more frequent the technique, the darker its shade in the visualization

7.) Based on the frequency of techniques and sub-techniques, the program also retrieves the top N (default: 5) recommended mitigation and detection measures from the MITRE ATT&CK website. The value of N can be customized in get_technique_information.py to suit the user's specific use case. The results are exported to an Excel file named defence_measure.xlsx."

8.) Please take note that this is a very basic program, feel free to make modification according to your needs and provide feedback.
