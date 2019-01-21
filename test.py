#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json

def get_next_pages_images(images, count, w, verbose):
    printt(verbose,"\nDownloading images from next page")
    for image in images:
    	print(image)
        #if "GraphImage" == image["node"]["__typename"]:
        #    urllib.request.urlretrieve(image["node"]["display_url"], foldername + "/" + str(count) + ".jpg")
         #   count += 1
        #    printt(verbose, ".", end=True)
        #    time.sleep(w)
    return count

class Insta_Image_Links_Scraper:

    def getlinks(self, hashtag, url):

        html = urllib.request.urlopen(url, context=self.ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        script = soup.find('script', text=lambda t: \
                           t.startswith('window._sharedData'))
        page_json = script.text.split(' = ', 1)[1].rstrip(';')
        data = json.loads(page_json)
        #with open('data.json', 'w') as outfile:
        #	json.dump(data, outfile)
        print ('Scraping links with #' + hashtag+"...........")

        user_id = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["id"]

        is_next = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]
        end_cursor = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]

        for post in data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
        	image_src = post['node']['thumbnail_resources'][4]['src']
        	#print(post['node']['shortcode'])
        	image_src= 'https://www.instagram.com/p/'+post['node']['shortcode']
        	print(image_src)
        	hs = open(hashtag + '.txt', 'a')
        	hs.write(image_src + '\n')
        	hs.close()
        
        #count = 0
        #wait_between_requests=1
        #verbose = False
        while is_next:
            next_url = 'https://www.instagram.com/graphql/query/?query_id=17888483320059182&variables=' \
                   '{"id":"' + user_id + '","first":12,"after":"' + end_cursor + '"}'
            hs = open(hashtag + '.txt', 'a')
            hs.write(next_url + '\n')
            hs.close()

            #response = None
            #html = urllib.request.urlopen(next_url, context=self.ctx).read()
            #soup = BeautifulSoup(html, 'html.parser')
            #script = soup.find('script', text=lambda t: \
            #               t.startswith('window._sharedData'))
            #page_json = script.text.split(' = ', 1)[1].rstrip(';')
            #data = json.loads(page_json)
            #for post in data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
        	#    image_src = post['node']['thumbnail_resources'][4]['src']
        	    #print(post['node']['shortcode'])
        	#    image_src= 'https://www.instagram.com/p/'+post['node']['shortcode']
        	#    hs = open(hashtag + '.txt', 'a')
        	#    hs.write(image_src + '\n')
        	#    hs.close()
            #with open('data1.json', 'w') as outfile:
            #    json.dump(data, outfile)
            #break

            response = requests.get(next_url, stream=True)
            #html = urllib.request.urlopen(next_url, context=self.ctx).read()
            #print(html)
            #data = response.json()
            print(response.headers['CONTENT-LENGTH'])
            break
            #json_obj = json.loads(response.text)
            #with open('data1.json', 'w') as outfile:
            #    json.dump(data, outfile)
            #break
            #images = json_obj["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
            #count = get_next_pages_images(images, count, wait_between_requests, verbose)

            #page_info = json_obj["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]
            #is_next = page_info["has_next_page"]
            #if is_next:
            #    end_cursor = page_info["end_cursor"]
        #print(next_url)
        #hs = open(hashtag + '.txt', 'a')
        #hs.write(next_url + '\n')
        #hs.close()

        #for post in data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
        	#image_src = post['node']['thumbnail_resources'][4]['src']
        #	print(post['node']['shortcode'])
        #	image_src= 'https://www.instagram.com/p/'+post['node']['shortcode']+
        #	hs = open(hashtag + '.txt', 'a')
        #	hs.write(image_src + '\n')
        #	hs.close()
        	#break
        #hs = open(hashtag + '.txt', 'a')
        #hs.write(data + '\n')
        #for post in data['entry_data']['TagPage'][0]['graphql'
        #        ]['hashtag']['edge_hashtag_to_media']['edges']:
            #image_src = post['node']['thumbnail_resources'][1]['src']
            #print(image_src)
         #   hs = open(hashtag + '.txt', 'a')
         #   hs.write(image_src + '\n')
        #    hs.close()

    def main(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

        #with open('hashtag_list.txt') as f:
        #    self.content = f.readlines()
        #self.content = [x.strip() for x in self.content]
        #for hashtag in self.content:
            #self.getlinks(hashtag,
             #             'https://www.instagram.com/explore/tags/'
             #             + hashtag + '/')
        self.getlinks('result',
                          'https://www.instagram.com/conkrightfarms/')


if __name__ == '__main__':
    obj = Insta_Image_Links_Scraper()
    obj.main()