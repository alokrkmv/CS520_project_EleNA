PURPLE='\033[0;35m'
BLUE='\033[0;34m' 
echo -e "${PURPLE}++++++++++++++++++++++++++ Running test suit for helper module +++++++++++++++++++++++++++++++++++++++++++++++++++ ${PURPLE}"
pytest helper_test.py
echo -e "${PURPLE}++++++++++++++++++++++++++ Running test suit for map generator module +++++++++++++++++++++++++++++++++++++++++++++"
pytest map_generator_tests.py
echo -e "${PURPLE}++++++++++++++++++++++++++ Running test suit for path finder module ++++++++++++++++++++++++++++++++++++++++++++++++"
pytest path_finder_test.py
echo -e "${BLUE}++++++++++++++++++++++++++++++++++++++++ Test Suit Executed successfully ++++++++++++++++++++++++++++++++++++++++++"