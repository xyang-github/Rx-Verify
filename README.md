# Rx Verify

This web application is prepared as a project for City College of California's CS 195 course. The purpose of Rx Verify 
is to create a tool where patients can keep an accurate record of medications, find resources pertaining to their 
medications, and run drug interactions. 

These combination of features is an attempt to improve health outcomes and empower patients with knowledge about their medications.

Technologies used:
<ul>
    <li>Framework: <a href="https://flask.palletsprojects.com/en/2.1.x/">Flask</a></li>
    <li>Database: <a href="https://sqlite.org/index.html">SQLite</a></li>
    <li>APIs from the <a href="https://lhncbc.nlm.nih.gov/RxNav/APIs/index.html">National Library of Medicine</a></li>
</ul>

Features implemented:
<ul>
    <li>Registration, login and password resetting</li>
    <li>Create, edit, delete and toggle list of active medications</li>
    <li>Generate a link to the National Library of Medicine for each active medication added</li>
    <li>Run drug interactions</li>
</ul>

How to run:
<ul>
<li>Follow instructions to clone the repository to your local machine <a href="https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository">here</a>.</li>
<li>Dependencies required are located in the <strong>requirements.txt</strong> file. Be sure to install these dependencies prior to running the application.</li>
<li>Set the environmental variables. This can be done in the command line/terminal, or within the IDE. For example, in the MacOS terminal:
<pre>
set FLASK_APP=rx_verify.py
set FLASK_ENV=development
</pre>
</li>
<li>Run flask
<pre>flask run</pre>
</li>


</ul>