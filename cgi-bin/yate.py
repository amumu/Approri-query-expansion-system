﻿##################################################################################
#                                                                                #
#  Copyright (c) 2013 Yao Nien, Yang, paulyang0125@gmail.com                     #  
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not   #
#  use this file except in compliance with the License. You may obtain a copy    #
#  of the License at http://www.apache.org/licenses/LICENSE-2.0. Unless required #
#  by applicable law or agreed to in writing, software distributed under the     #
#  License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS  #
#  OF ANY KIND, either express or implied. See the License for the specific      #
#  language governing permissions and limitations under the License.             # 
#                                                                                #
##################################################################################

from string import Template



def render_seg_result(results):
    with open('templates/debug_result.html') as headf:
        result_text = headf.read()
    debug_result = Template(result_text)
    return(debug_result.substitute(seg_result = results))

def render_search_result(each_title,each_content,each_link):
    with open('templates/search_result.html') as headf:
        result_text = headf.read()
    search_result = Template(result_text)
    return(search_result.substitute(title = each_title,content = each_content,link = each_link))

def start_response(resp="text/html"):
    return('Content-type: ' + resp + '\n\n')

def include_header(the_title):
    with open('templates/header.html') as headf:
        head_text = headf.read()
    header = Template(head_text)
    return(header.substitute(title=the_title))

def include_footer(the_links):
    with open('templates/footer.html') as footf:
        foot_text = footf.read()
    link_string = ''
    for key in the_links:
        link_string += '<a href="' + the_links[key] + '">' + key + '</a>&nbsp;&nbsp;&nbsp;&nbsp;'
    footer = Template(foot_text)
    return(footer.substitute(links=link_string))

def start_form(the_url, form_type="POST"):
    return('<form action="' + the_url + '" method="' + form_type + '">')

def end_form(submit_msg="Submit", submitname = "submit"):
    return('<input type=submit name="' + submitname + '"' + ' value="' + submit_msg + '">')
	
	
def input_button(rb_value, rb_url):
    return('<input type="button" ' + '" value="' + rb_value + '" onclick="' + rb_url + '"> ' + '<br />')
def input_text(text_name, text_value):
    return('<p></p><input type="text"  name="' + text_name +  '" value="' + text_value + '"> '+ '<br />')
	
def radio_button(rb_name, rb_value):
    return('<input type="radio" name="' + rb_name +
                             '" value="' + rb_value + '"> ' + rb_value + '<br />')

def radio_button_id(rb_name, rb_value, rb_id):
    return('<input type="radio" name="' + rb_name +
                             '" value="' + str(rb_id) + '"> ' + rb_value + '<br />')

def u_list(items):
    u_string = '<ul>'
    for item in items:
        u_string += '<h3>' + '<li>' + item + '</li>' + '<h3>'
    u_string += '</ul>'
    return(u_string)

def header(header_text, header_level=1):
    return('<h' + str(header_level) + '>' + header_text +
           '</h' + str(header_level) + '>')

def para(para_text):
    return('<p>' + para_text + '</p>')

def create_inputs(inputs_list):
    html_inputs = ''
    for each_input in inputs_list:
        html_inputs = html_inputs + '<input type="Text" name="' + each_input + '" size=40>'
    return(html_inputs)

def do_form(name, the_inputs, method="POST", text="Submit"):
    with open('templates/form.html') as formf:
        form_text = formf.read()
    inputs = create_inputs(the_inputs)
    form = Template(form_text)
    return(form.substitute(cgi_name=name,
                           http_method=method,
                           list_of_inputs=inputs,
                           submit_text=text))
def include_menu(the_links, query):
    with open('templates/menu.html') as menuf:
        menu_text = menuf.read()
    link_string = ''
    for key in the_links:
        link_string += '<a href="' + the_links[key] + '">' + key + '</a>&nbsp;&nbsp;&nbsp;&nbsp;'
    menu = Template(menu_text)
    return(menu.substitute(menu_links=link_string, orignal_query=query ))

def include_menu1(the_links, expandedWordList):
    with open('templates/menu1.html') as menuf:
        menu_text = menuf.read()
    link_string = ''
    for key in the_links:
        link_string += '<a href="' + the_links[key] + '">' + key + '</a>&nbsp;&nbsp;&nbsp;&nbsp;'
    menu = Template(menu_text)
    return(menu.substitute(menu_links=link_string, orignal_query=query ))

def hidden_input(name, value): # value = covert utf-8 string to STR 
	return('<input type="hidden" name="' + name + '" value="' + value + '"> ')

def createLink(the_links):
	link_string = ''
	for key in the_links:
		link_string += '<a href="' + the_links[key] + '">' + key + '</a>&nbsp;&nbsp;&nbsp;&nbsp;'
	return(link_string)
