# MD5 MATCHER

Script used for matching files from one directory with files of another, comparing by md5 hashsum

------------
### Use case
QA signed artifacts on infra-web (some final RC build), then artifacts were pushed into PIMS and edelivery.
#### Goal: you want to confirm that proper artifacts were uploaded from infra-web to pims/edelivery

<br>**Terminology**:
- **STAGING** - some files from infra-web that qa signed off (**staging_path**)
- **VERIFICATION** - some files from pims ftp or edelivery (**verification_path**)

------------
### Requirements
- Python3

### Guide
1. on **infra-web** find signed off artifacts (leads, managers should have correct link) and download them all into some location, for example under /opt/staging.
<br>This will be your **staging_path**
<br>You can save that artifacts into different subdirectories if needed 
2. download all artifacts that were pushed into PIMS/Edelivery, for example under /opt/edelivery.
<br>This will be your **verification_path**
<br>You can save that artifacts into different subdirectories if needed
3. edit md5_matcher_config.properties, and set **staging_path**, **verification_path** as directories used in #1 and #2. 
- Win example:
<br>`staging_path=d:/Downloads/staging`
<br>`verification_path=d:/Downloads/edelivery`


- Linux example:
<br>`staging_path=/opt/staging`
<br>`verification_path=/opt/edelivery`

4. set which file extensions matcher should ignore. For example, you might want to skip txt, pdf and md5 files as usually we check them separately, then you have to set it as a comma-separated list, like:
<br>`matcher_skip_extensions=txt,pdf,md5`
<br>note, if nothing was specified - any file types will be compared
5. run matcher:
- Linux:
<br>`python3 md5_matcher.py` 
- Win:
<br>`python md5_matcher.py`
6. check output results for details

### NOTES
- you can have multiple subdirectories in staging or verification paths, md5checker will iterate through each file.
- artifact file names can have different names, but if they have the same MD5, then we treat them as a same file
- it's possible that one signed artifact is part of different packages on edelivery, so one file can have a couple of matches with the different paths, read the output for details, it can have output like:
<br>
`FOUND MATCHES:`
<br>`d:/Downloads/qa_signed\jrio-1.0.1-linux.zip                                 | ['d:/Downloads/pims/staged\\jrio-1.0.1-linux.zip', 'd:/Downloads/pims/staged\\package2\\jrio-1.0.1-linux.zip']`
<br>`d:/Downloads/qa_signed\TIB_js-jrio_1.1.0_linux_x86_64.zip                   | ['d:/Downloads/pims/staged\\package1\\TIB_js-jrio_1.1.0_linux_x86_64.zip', 'd:/Downloads/pims/staged\\package2\\TIB_js-jrio_1.1.0_linux_x86_64.zip']`