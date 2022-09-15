#!/usr/bin/env python3

from urllib.parse import quote as urlquote
from datetime import datetime

def block_tweet(text):
	"text가 들어있는 트윗을 거른다."
	return "twitter.com#?#article[data-testid=tweet]:-abp-contains({})".format(text)

def block_usercell(text):
	"유저 프로필 목록(팔로잉/팔로워, 유저 검색결과 등)에서 text가 들어있으면 거른다."
	return "twitter.com#?#div[data-testid=UserCell]:-abp-contains({})".format(text)

def block_trend(text):
	"실시간 트렌드 목록에 text가 들어있으면 거른다."
	return "twitter.com#?#div[data-testid=trend]:-abp-contains({})".format(text)

def block_typeahead(text):
	"검색창 하단의 목록에서 text가 들어있는 항목을 거른다."
	return "twitter.com#?#div[data-testid=typeaheadResult]:-abp-contains({})".format(text)

now = datetime.now().strftime("%Y.%m.%d.%H%M%S")

header = f"""[Adblock Plus 2.0]
! Homepage: https://github.com/gaeulbyul/K-SpamTweetFilter
! Title: K-SpamTweetFilter
! Author: 가을별 <Gaeulbyul>
! Expires: 12 hours
! Version: {now}

! 참고: 이 파일을 자동적으로 생성되었습니다.
"""

smallquote = "'"
largequote = "\""

def preprocess(text):
	# 정규식
	if text.startswith("/") and text.endswith("/"):
		return text
	# 따옴표
	elif largequote in text and smallquote in text:
		return largequote + text.replace(largequote, "\\\"") + largequote
	elif largequote in text:
		return smallquote + text + smallquote
	else:
		return largequote + text + largequote

def main():
	print("Reading from SPAM_WORDS.txt ...")
	with open("SPAM_WORDS.txt", "r", encoding="UTF8") as inputfile:
		spamwords = inputfile.readlines()
	print("Writing to FILTER.txt ...")
	count = 0
	with open("FILTER.txt", "w", encoding="UTF8") as filterfile:
		filterfile.write(header)
		for line in spamwords:
			line = line.strip()
			if line == "":
				continue
			# 괄호로 감싼 줄을 주석으로 취급하여 건너뛴다.
			if line.startswith("(") and line.endswith(")"):
				continue
			count += 1
			line = preprocess(line)
			filterfile.write(block_tweet(line) + "\n")
			filterfile.write(block_usercell(line) + "\n")
			filterfile.write(block_trend(line) + "\n")
			filterfile.write(block_typeahead(line) + "\n")
			filterfile.write("\n")
	print(f"DONE. (rules: {count})")

if __name__ == "__main__":
	main()
