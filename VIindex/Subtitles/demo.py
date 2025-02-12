def get_timeline_subtitles(video_id, subtitles, timeline):

    from youtube_transcript_api import YouTubeTranscriptApi

    data = YouTubeTranscriptApi.get_transcript(video_id)

    for data_item in data:
        sentence = data_item["text"]
        start = data_item["start"]
        durration = data_item["duration"]
        num_words = 0
        
        for ch in sentence:
            if ch==' ' or ch == '/n':
                num_words+=1
        word_durration = 0
        if num_words != 0: 
            word_durration = durration/num_words
        count = 0
        word = ""
        for ch in sentence:
            if ch == ' ' or ch == '/n':
                subtitles.append(word)
                timeline.append(start+count*word_durration)
                count+=1            
                word = ""
            else :
                word+=ch

    return

def edit_distance(str1, str2):
    m = len(str1)
    n = len(str2)
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]
 
    for i in range(m + 1):
        for j in range(n + 1):
 
            if i == 0:
                dp[i][j] = j    
 
            elif j == 0:
                dp[i][j] = i    
 
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
 
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                   dp[i-1][j],        # Remove
                                   dp[i-1][j-1])    # Replace
 
    return dp[m][n]

def get_synonyms(word):
    import nltk
    from nltk.corpus import wordnet   #Import wordnet from the NLTK
    syn = list()

    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            syn.append(lemma.name())    #add the synonyms
        
    return syn


def find_timeline_ind(start,end,words,subtitles,timeline):
    synonym_words = list()
    for word in words:
        synonym_words = synonym_words + get_synonyms(word)
    
    total_count = 0

    for i in range(start,end+1):
        curr_word = subtitles[i]
        count = 0
        for word in synonym_words:
            if edit_distance(curr_word,word) <= 1:
                count = 1
                break 
        # if word in synonym_words:
        #     count = 1
        total_count += count

    exepected_count = 0.2*total_count
    # if total_count == 1:
        # print(-2)

    for i in range(start,end+1):
        curr_word = subtitles[i]
        count = 0
        for word in synonym_words:
            if edit_distance(curr_word,word) <= 1:
                count = 1
                break 
        # if word in synonym_words:
        #     count = 1

        exepected_count -= count
        if exepected_count <= 0.1:
            return i
    
    print(-1)
    return start

#video id for which you need indexing

# video_id = "https://youtu.be/TVhNuFbUs6k"
#video_id = "H4YcqULY1-Q"

#video_id for index.txt indexing
video_id = "yfsTZbwgMSE"
video_id = "E_IQ3mzZyrw" 

subtitles = list()
timeline = list()
get_timeline_subtitles(video_id,subtitles,timeline)

# print(subtitles)
# print(timeline)


index_file = "index.txt"
file_text = open(index_file,"r").read()
indexes = []
line = ""
words = list()
word = ""
index_timeline = [0.00]
start_ind = 0
end_ind = len(timeline)-1


for ch in file_text:

    if ch == " " or ch == '\n':
        if len(word) > 2 :
            words.append(word)
        word = ""

    else :
        word = word + ch


    if ch == '\n':
        next_ind_timeline = find_timeline_ind(start_ind,end_ind,words,subtitles,timeline)
        next_timeline = timeline[next_ind_timeline]
        start_ind = next_ind_timeline
        index_timeline.append(next_timeline)
        indexes.append(line)
        line = ""
        words.clear()
    else :
        line += ch


# next_ind_timeline = find_timeline_ind(start_ind,end_ind,words,subtitles,timeline)
# next_timeline = timeline[next_ind_timeline]
# start_ind = next_ind_timeline
# index_timeline.append(next_timeline)
# indexes.append(line)
# line = ""
# words.clear()
    
# print(indexes)
for i in range(len(index_timeline)):
    index_timeline[i] = float((index_timeline[i]//60) + 0.01*(index_timeline[i]%60))
# print(index_timeline)
for i in range(len(indexes)):
    print('%.2f'%index_timeline[i],indexes[i])
# # print(words)


# words_keys = list(words.keys())
# # print(words_keys)
# word_in_subtitles = ""
# for ch_in_subtitles in subtitles:
#     if ch_in_subtitles == " " or ch_in_subtitles == "\n":
#         if word_in_subtitles in words_keys:
#             words[word_in_subtitles] = words[word_in_subtitles] + 1

#         # print(word_in_subtitles)
#         # print("123 ")
#         word_in_subtitles = ""
#     else :
#         word_in_subtitles += ch_in_subtitles


# print(subtitles)
# print(words)


# for index in indexes:
