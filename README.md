# MD5 MATCHER

Automation for matching files from one directory with files another

------------
### Use-case
QA signed artifacts on infra-web (some build), artifacts are pushed into PIMS and edelivery. **Terminology**:
- **STAGING** - some files from infra-web that qa signed
- **VERIFICATION** - some files from pims ftp or edelivery 

#### Goal: to verify that proper artifacts were pushed into pims/edelivery

------------
### Usage
1. download artifacts that were signed off into some location, for example under /opt/staging.
2. download artifcats that were pushed into PIMS/Edelivery
3. edit md5_matcher_config.properties, and set **staging_path**, **verification_path** to directories for #1 and #2. 
Win example: ` staging_path=d:/Downloads/staging/qa`
Linux example: `staging_path=/opt/staging/qa`
4. set which file extensions matcher should ignore, comma-separated list, if nothing specified - all file types are matched
5. run matcher:
Linux: `python3 md5_matcher.py`
Win: `python md5_matcher.py`
6. check output results for details

**NOTE**: you can have multiple subdirectories in staging or verification paths, md5checker will iterate through each file