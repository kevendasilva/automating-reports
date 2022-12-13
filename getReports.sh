#! /bin/bash

echo "The script is starting! Sit down and wait for your new reports, astronaut."
echo
echo "Let's start with site information!"

sleep 3

python3 src/edit_data/app.py

while :
do
  echo "Start producing reports? (S/n) "
  read INPUT_STRING
  case $INPUT_STRING in
    S)
      echo "The process is about to start!"

      ruby src/get_reports/app.rb

      echo "We have reached the end of another mission! 🚀"
      sleep 2
      echo "Check the reports folder."

      break
      ;;
    n)
      echo "See you next time, astronaut 👨‍🚀👩‍🚀."
      break
      ;;
    *)
      echo "Sorry, I don't understand"
      ;;
  esac
done
