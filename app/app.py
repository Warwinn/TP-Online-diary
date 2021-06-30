#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""app.py: Code for Streamlit."""

__author__ = "Dewynter Antoine AKA Warwin"
__credits__ = ["Dewynter Antoine AKA Warwin"]
__version__ = "1.0"
__status__ = "Developement"

import datetime
import streamlit as st
import requests
import matplotlib.pyplot as plt

def list_client():
    """Visualisation of api function"""
    req = requests.get('http://127.0.0.1:8000/list_user/')
    st.dataframe(req.json())

def create_user():
    """Visualisation of api function"""
    with st.form("Renseignements"):
        max_date = datetime.datetime.today()
        min_date = datetime.datetime.today()-datetime.timedelta(days=150*365)
        user_name = st.text_input('user_name :', max_chars=55, help='Champ obligatoire')
        last_meet = st.date_input('last_meet', min_value=min_date, max_value=max_date, help='Champ obligatoire')
        last_meet = datetime.datetime.combine(last_meet, datetime.time())
        next_meet = st.date_input('next_meet', min_value=min_date, max_value=max_date, help='Champ obligatoire')
        next_meet = datetime.datetime.combine(next_meet, datetime.time())
        submitted = st.form_submit_button("Submit")
        if submitted:
            if user_name :
                url = f'?prenom={user_name}'
                if last_meet:
                    url = url+f'&last_meet={last_meet}'
                if next_meet:
                    url = url+f'&next_meet={next_meet}'
                requests.post(f'http://127.0.0.1:8000/create_user/{url}')
                st.success('User add')
            else:
                st.warning('Remplissez tous les champs obligatoires svp')

def read_user():
    """Visualisation of api function"""
    user_id = st.text_input('user_id :', max_chars=55, help='Champ obligatoire')
    if user_id:
        req = requests.get (f'http://127.0.0.1:8000/read_user/{user_id}')
        st.dataframe(req.json())

def update_user():
    """Visualisation of api function"""
    with st.form("Renseignements"):
        user_id = st.text_input('user_id :', max_chars=55, help='Champ obligatoire')
        max_date = datetime.datetime.today()
        min_date = datetime.datetime.today()-datetime.timedelta(days=150*365)
        user_name = st.text_input('user_name :', max_chars=55, help='Champ obligatoire')
        last_meet = st.date_input('last_meet', min_value=min_date, max_value=max_date, help='Champ obligatoire')
        last_meet = datetime.datetime.combine(last_meet, datetime.time())
        next_meet = st.date_input('next_meet', min_value=min_date, max_value=max_date, help='Champ obligatoire')
        next_meet = datetime.datetime.combine(next_meet, datetime.time())
        submitted = st.form_submit_button("Submit")
        if submitted:
            if user_id:
                if user_name or last_meet or next_meet:
                    url = ''
                    if user_name:
                        url = url + f'user_name={user_name}&'
                    if last_meet:
                        url = url + f'last_meet={last_meet}&'
                    if next_meet:
                        url = url + f'next_meet={next_meet}&'
                    url = url[:-1]
                    requests.put(f'http://127.0.0.1:8000/update_user/{user_id}?{url}')
                    st.success('Votre message a bien été modifié.')
                else:
                    st.warning('Renseignez au moins un champ à modifier')
            else:
                st.warning('Renseignez l\'id de l\'utilisateur à modifier')

def delete_user():
    """Visualisation of api function"""
    user_id = st.text_input('user_id :', max_chars=55, help='Champ obligatoire')
    if user_id:
        req = requests.get (f'http://127.0.0.1:8000/delete_user/{user_id}')
        st.dataframe(req.json())

def create_message(user_id):
    """Visualisation of api function"""
    text = st.text_input('Quelle est votre message aujourd\'hui ?', max_chars=280)
    if text:
        requests.post(f'http://127.0.0.1:8000/create_message/{user_id}?dm_text={text}')
        st.success('Votre message a bien été envoyé.')

def update_message(user_id):
    """Visualisation of api function"""
    text = st.text_input('Quelle est votre message ?', max_chars=280)
    if text:
        requests.put(f'http://127.0.0.1:8000/edit_message/{user_id}?dm_text={text}')
        st.success('Votre message a bien été mis à jour.')

def read_message(user_id):
    """Visualisation of api function"""
    req = requests.get(f'http://127.0.0.1:8000/read_message/{user_id}')
    st.write('Votre message du jour est:   \n   ', req.json()[0][2])

def list_message():
    """Visualisation of api function"""
    req = requests.get(f'http://127.0.0.1:8000/list_message/{user_id}')
    st.dataframe(req.json())

def read_message_emotion():
    """Visualisation of api function"""
    with st.form("Renseignements"):
        user_id = st.text_input('Id du client :', help='Champ obligatoire')
        date = st.date_input('date', help='Champ obligatoire')
        submitted = st.form_submit_button("Submit")
        if submitted :
            req = requests.get(f'http://127.0.0.1:8000/read_message_emotion/{user_id}?dm_datetime={date}')
            st.write('Message: ' + req.json()[0]['dm_text'])
            st.write('Sentiment majoritaire: ' + req.json()[0]['dm_emotion'])
            labels = ['dm_prob_anger','dm_prob_fear','dm_prob_happy','dm_prob_love','dm_prob_sadness','dm_prob_surprise']
            rates = [req.json()[0][label] for label in labels]
            labels2 = ['anger','fear','happy','love','sadness','surprise']
            plt.pie(rates, autopct="%.1f%%", radius=3)
            plt.title('Répartition des émotions')
            my_circle=plt.Circle( (0,0), 1.2, color='white')
            p=plt.gcf()
            p.gca().add_artist(my_circle)
            plt.legend(labels2, loc='best')
            plt.axis('equal')
            fig = plt.gcf()
            st.pyplot(fig)
            plt.close()

def read_message_emotion_periode():
    """Visualisation of api function"""
    with st.form("Renseignements"):
        user_id = st.text_input('Id du client :', help='Champ obligatoire')
        date_debut = st.date_input('last_meet', help='Champ obligatoire')
        date_fin = st.date_input('last_meet', help='Champ obligatoire')
        submitted = st.form_submit_button("Submit")
        if submitted :
            req = requests.get(f'http://127.0.0.1:8000/read_moyenne_emotion_periode/{user_id}?debut_dm_datetime={date_debut}&fin_dm_datetime={date_fin}')
            st.write('Message: ' + req.json()[0]['dm_text'])
            st.write('Sentiment majoritaire: ' + req.json()[0]['dm_emotion'])
            labels = ['dm_prob_anger','dm_prob_fear','dm_prob_happy','dm_prob_love','dm_prob_sadness','dm_prob_surprise']
            rates = [req.json()[0][label] for label in labels]
            labels2 = ['anger','fear','happy','love','sadness','surprise']
            plt.pie(rates, autopct="%.1f%%", radius=3)
            plt.title('Répartition des émotions')
            my_circle=plt.Circle( (0,0), 1.2, color='white')
            p=plt.gcf()
            p.gca().add_artist(my_circle)
            plt.legend(labels2, loc='best')
            plt.axis('equal')
            fig = plt.gcf()
            st.pyplot(fig)
            plt.close()

st.title("Online diary")
Pages = ['Coach','Utilisateur',]
page = st.sidebar.radio('Page', Pages)

objectif_clients = ['Ajouter un texte', 'Modifier un texte', 'Lire son texte']
objecitf_coach = ['Gestion des informations', 'Visualisation']
choix_gestion = ['Ajouter', 'Modifier', 'Supprimer']
choix_visu = ['Liste Client','Infos clients', 'Liste des messages', 'Ressenti à une date', 'Ressenti sur une période']

if page == Pages[0]:
    st.header("Coach")
    selec_coach = st.selectbox('Que souhaitez-vous faire ?', objecitf_coach)
    if selec_coach == objecitf_coach[0]:
        selec_gestion = st.radio('Choisissez la modification à effectuer: ', choix_gestion)
        if selec_gestion == choix_gestion[0]:
            create_user()
        if selec_gestion == choix_gestion[1]:
            update_user()
        if selec_gestion == choix_gestion[2]:
            delete_user()
    if selec_coach == objecitf_coach[1]:
        selec_visu = st.radio('Que souhaitez-vous faire ?', choix_visu)
        if selec_visu == choix_visu[0]:
            list_client()
        if selec_visu == choix_visu[1]:
            read_user()
        if selec_visu == choix_visu[2]:
            list_message()
        if selec_visu == choix_visu[3]:
            read_message_emotion()
        if selec_visu == choix_visu[4]:
            read_message_emotion_periode()

if page == Pages[1]:
    st.header("Utilisateur")
    user_id = st.text_input('Quel est votre ID ?')
    if user_id :
        st.write(f'Bonjour {user_id}, bienvenue dans votre journal en ligne')
        selec_client = st.radio('Que souhaitez-vous faire ?', objectif_clients)
        if selec_client == objectif_clients[0]:
            create_message(user_id)
        if selec_client == objectif_clients[1]:
            update_message(user_id)
        if selec_client == objectif_clients[2]:
            read_message(user_id)
