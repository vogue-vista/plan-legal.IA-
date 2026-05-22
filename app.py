import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# -------------------------
# CONFIGURATION DE LA PAGE
# -------------------------
st.set_page_config(page_title="Légal-AI Pro", page_icon="⚖️", layout="wide")

# Design épuré et suppression de la sidebar
st.markdown("""
<style>
[data-testid="stSidebar"] {display: none !important;}
[data-testid="stSidebarNav"] {display: none !important;}
@import url('https://googleapis.com');
html, body, div, p, h1, h2, h3, h4, h5, h6, span {
    font-family: 'Poppins', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# CONFIGURATION PAYPAL
# -------------------------
PAYPAL_CLIENT_ID = "DEMO"  
PAYPAL_PLAN_ID = "DEMO"    

# -------------------------
# GESTION DE L'ACCÈS
# -------------------------
if "est_abonne" not in st.session_state:
    st.session_state.est_abonne = False

try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    API_KEY = ""

# -------------------------
# INTERFACE SÉCURISÉE
# -------------------------
st.title("⚖️ Légal-AI Pro")
st.subheader("Générez vos CGV, Mentions Légales et Politiques de Confidentialité conformes en 2 secondes.")

# CAS 1 : L'UTILISATEUR N'A PAS PAYÉ
if not st.session_state.est_abonne:
    st.warning("🔒 Cette application est réservée aux membres de la version Premium.")
    
    col_offre, col_connexion = st.columns(2, gap="large")
    
    with col_offre:
        st.subheader("🚀 Sécurisez votre business pour 30 $/mois")
        st.write("Évitez les amendes et protégez votre site web ou e-commerce. Générez des documents juridiques sur-mesure sans payer des centaines d'euros d'avocat.")
        st.write("Le paiement est entièrement sécurisé par **PayPal**.")
        
        if PAYPAL_CLIENT_ID == "DEMO":
            paypal_html = """
            <a href="https://paypal.com" target="_blank" style="text-decoration: none;">
                <div style="background-color: #ffc439; color: #003087; text-align: center; 
                            padding: 12px; font-family: Arial, sans-serif; font-weight: bold; 
                            border-radius: 4px; max-width: 300px; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    🟨 S'abonner avec PayPal (Démo)
                </div>
            </a>
            """
        else:
            paypal_html = f"""
            <div id="paypal-button-container-fixed" style="max-width: 350px; margin-top: 20px;"></div>
            <script src="https://paypal.com/sdk/js?client-id={PAYPAL_CLIENT_ID}&vault=true&intent=subscription" data-sdk-integration-source="button-factory"></script>
            <script>
              paypal.Buttons({{
                  style: {{ shape: 'rect', color: 'gold', layout: 'vertical', label: 'subscribe' }},
                  createSubscription: function(data, actions) {{
                    return actions.subscription.create({{ 'plan_id': '{PAYPAL_PLAN_ID}' }});
                  }},
                  onApprove: function(data, actions) {{
                    alert('Abonnement réussi ! ID : ' + data.subscriptionID);
                  }}
              }}).render('#paypal-button-container-fixed');
            </script>
            """
        components.html(paypal_html, height=150, scrolling=False)
        
    with col_connexion:
        st.subheader("🔑 Déjà abonné ?")
        email = st.text_input("Adresse e-mail")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        
        if st.button("Se connecter", use_container_width=True):
            if email == "test@client.com" and mot_de_passe == "legal30":
                st.session_state.est_abonne = True
                st.success("Accès accordé !")
                st.rerun()
            else:
                st.error("Identifiants incorrects.")

# CAS 2 : L'UTILISATEUR EST ABONNÉ -> ACCÈS COMPLÈT
else:
    st.write("✨ **Espace Juridique Actif.** Protégez votre activité dès maintenant.")
    if st.button("🚪 Se déconnecter", key="logout"):
        st.session_state.est_abonne = False
        st.rerun()
        
    st.write("---")

    with st.container(border=True):
        col_inputs, col_options = st.columns(2)
        
        with col_inputs:
            nom_entreprise = st.text_input("Nom de l'entreprise ou du site web :", placeholder="Ex: MyShop S.A.S, Jean Dupont Freelance")
            infos_boite = st.text_area(
                "Informations clés (Adresse, capital social, contact) :", 
                placeholder="Ex: 12 Rue de la Paix Paris, Capital de 1000€, email: contact@myshop.com"
            )
            
        with col_options:
            document_choix = st.selectbox("Document à générer", [
                "📜 Conditions Générales de Vente (CGV - E-commerce)",
                "💼 Conditions Générales d'Utilisation (CGU - Site vitrine / Blog)",
                "🔒 Politique de Confidentialité & RGPD",
                "📝 Mentions Légales Obligatoires"
            ])
            
            details_specifiques = st.selectbox("Politique de livraison et retours", [
                "Livraison 48h, retours gratuits sous 14 jours",
                "Pas de livraison physique (Prestation de service / Produits digitaux)",
                "Livraison internationale, retours à la charge du client"
            ])

        generer = st.button("🚀 Générer le Document Légal", use_container_width=True)

    if generer:
        if not API_KEY:
            st.error("⚠️ Erreur : La clé GROQ_API_KEY est manquante dans les Secrets.")
        elif not nom_entreprise:
            st.error("⚠️ Veuillez entrer le nom de votre entreprise ou site web.")
        else:
            with st.spinner("L'IA de Groq rédige votre document juridique officiel..."):
                try:
                    client = Groq(api_key=API_KEY)
                    
                    prompt_systeme = """Tu es un avocat expert en droit du numérique, RGPD et e-commerce.
                    Ton but est de rédiger des documents juridiques rigoureux, conformes aux lois, clairs et structurés.
                    Utilise une structure professionnelle avec des articles numérotés (Article 1 : Objet, Article 2 : Prix, etc.).
                    Ajoute un avertissement au début expliquant que ce document est généré par IA et doit être vérifié par un professionnel du droit.
                    Ne fais aucune introduction ni conclusion amicale, commence directement par le document."""

                    prompt_utilisateur = f"""
                    Nom du site/entreprise : {nom_entreprise}
                    Coordonnées de l'entreprise : {infos_boite}
                    Type de document : {document_choix}
                    Politique spécifique (Livraison/Retours) : {details_specifiques}
                    """

                    reponse = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": prompt_systeme},
                            {"role": "user", "content": prompt_utilisateur}
                        ],
                        temperature=0.5 # Température plus basse pour être très factuel et précis (juridique)
                    )
                    
                    # Code d'extraction sécurisé avec l'index [0] pour éviter l'erreur de liste
                    doc_genere = reponse.choices[0].message.content
                    st.success("✨ Votre document juridique est prêt !")
                    st.markdown(doc_genere)
                    st.text_area("Copier le texte brut :", value=doc_genere, height=300)

                except Exception as e:
                    st.error(f"Erreur technique Groq : {str(e)}")
