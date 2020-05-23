# coding=utf-8
from django.contrib.auth.models import User
from backend_citizen.tests import BackendCitizenTestCaseBase, PASSWORD
from django.urls import reverse
from organization_profiles.models import OrganizationTemplate, ExtraPage, LOGO_SIZE
from popular_proposal.models import PopularProposal, ProposalLike
from django.test import override_settings
from elections.models import Candidate
from django.contrib.sites.models import Site
from django.test import override_settings


class OrganizationFrontEndTestCase(BackendCitizenTestCaseBase):
    def setUp(self):
        super(OrganizationFrontEndTestCase, self).setUp()
        self.user = User.objects.create(username='ciudadanoi',
                                        first_name='Ciudadano Inteligente',
                                        email='mail@mail.com')
        self.user.set_password(PASSWORD)
        self.user.save()
        self.user.profile.is_organization = True
        self.user.profile.save()

    def test_properties(self):
        url = reverse('organization_profiles:home', kwargs={'slug': self.user.username})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_no_template_return_404(self):
        url = reverse('organization_profiles:home', kwargs={'slug': self.user.username})
        self.user.organization_template.delete()
        self.user.profile.is_organization = False
        self.user.profile.save()
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_return_basic_data(self):
        self.user.organization_template.content = u'<h1>{{object}}</h1>'
        self.user.organization_template.save()
        url = reverse('organization_profiles:home', kwargs={'slug': self.user.username})
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        self.assertIn(u"<h1>" + str(self.user) + u"</h1>", content)
        '''Y si ahora le cambio el template debería ser distinto o no?????'''
        self.user.organization_template.content = u'<h2>{{object}}</h2>'
        self.user.organization_template.save()
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        self.assertIn(u"<h2>" + str(self.user) + u"</h2>",
                      content,
                      u"Cambiando el template handlebars cambiar la respuesta")
        '''Y si ahora le cambio el template debería ser distinto o no?????'''
        self.user.organization_template.content = ""
        self.user.organization_template.save()
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        self.assertTrue(content, "Si está vacio entonces dibuja el contenido de organization_detail_view.hbs")


    @override_settings(ORGANIZATION_TEMPLATES_USING_HBS=False)
    def test_return_basic_data_as_html(self):
        url = reverse('organization_profiles:home', kwargs={'slug': self.user.username})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'organization_profiles/detail.html')

    def test_display_basic_data(self):
        self.user.organization_template.logo = self.get_image()
        self.user.organization_template.facebook = u'https://www.facebook.com/ciudadanointeligente'
        self.user.organization_template.secondary_color = '#EEEEDD'
        c = u'<ul><li>logo:{{logo}}</li><li>facebook:{{facebook}}</li><li>secondary:{{secondary_color}}</li></ul>'
        self.user.organization_template.content = c
        self.user.organization_template.save()
        url = reverse('organization_profiles:home', kwargs={'slug': self.user.username})
        response = self.client.get(url)
        content = response.context
        self.assertEquals(self.user.organization_template.logo.url, content['logo'])
        self.assertEquals(self.user.organization_template.facebook, content['facebook'])
        self.assertEquals(self.user.organization_template.secondary_color, content['secondary_color'])

    def test_when_is_owner(self):
        self.user.organization_template.logo = self.get_image()
        self.user.organization_template.facebook = u'https://www.facebook.com/ciudadanointeligente'
        self.user.organization_template.secondary_color = '#EEEEDD'
        c = u'<ul><li>logo: {{logo}}</li><li>facebook: {{facebook}}</li><li>secondary c: {{secondary_color}}</li></ul>'
        self.user.organization_template.content = c
        self.user.organization_template.save()
        url = reverse('organization_profiles:home', kwargs={'slug': self.user.username})
        response = self.client.get(url)
        context = response.context
        self.assertFalse(context['is_owner'])
        logged_in = self.client.login(username=self.user.username, password=PASSWORD)
        self.assertTrue(logged_in)
        response = self.client.get(url)
        context = response.context
        self.assertTrue(context['is_owner'])


class OrganizationTemplateTestCase(BackendCitizenTestCaseBase):
    def setUp(self):
        super(OrganizationTemplateTestCase, self).setUp()
        self.user = User.objects.create(username='ciudadanoi',
                                        password=PASSWORD,
                                        email='mail@mail.com')

    def test_instanciate_model(self):
        self.user.first_name = 'Fundacion'
        self.user.last_name = 'Ciudadano Inteligente'
        self.user.profile.is_organization = True
        self.user.profile.save()
        #  Acá se crea un OrganizationTemplate
        # y se crea porque en la linea anterior le dijimos que la wea era organización
        template = OrganizationTemplate.objects.get(organization=self.user)
        self.assertEquals(template.content, "")
        self.assertEquals(template.title, "Fundacion Ciudadano Inteligente")
        fiera = User.objects.create(username='fiera_feroz',
                                    password=PASSWORD,
                                    email='fiera@mail.com')
        fiera.profile.is_organization = False
        fiera.profile.save()
        self.assertFalse(OrganizationTemplate.objects.filter(organization=fiera))
        self.assertIn(str(self.user), str(template))

    def test_get_image(self):
        self.user.first_name = 'Fundacion'
        self.user.last_name = 'Ciudadano Inteligente'
        self.user.profile.is_organization = True
        self.user.profile.save()
        #  Acá se crea un OrganizationTemplate
        # y se crea porque en la linea anterior le dijimos que la wea era organización
        template = OrganizationTemplate.objects.get(organization=self.user)
        self.assertTrue(template.get_shared_image())
        self.assertTrue(template.ogp_image())

    def test_change_image_size(self):
        self.user.first_name = 'Fundacion'
        self.user.last_name = 'Ciudadano Inteligente'
        self.user.profile.is_organization = True
        self.user.profile.save()
        #  Acá se crea un OrganizationTemplate
        # y se crea porque en la linea anterior le dijimos que la wea era organización
        template = OrganizationTemplate.objects.get(organization=self.user)
        template.logo = self.get_image()
        template.save()

        template.generate_logo_small()
        self.assertEquals(template.logo_small.height, LOGO_SIZE)

        self.assertEquals(template.logo_small.width, LOGO_SIZE)

    @override_settings(DEFAULT_EXTRAPAGES_FOR_ORGANIZATIONS=[{'title': u'Agenda', 'content': 'Esta es la agenda'},
                                                             {'title': u'Documentos', 'content': 'Documentos'}])
    def test_automatically_create_extra_pages(self):
        self.user.profile.is_organization = True
        self.user.profile.save()
        #  Acá se crea un OrganizationTemplate
        # y se crea porque en la linea anterior le dijimos que la wea era organización
        OrganizationTemplate.objects.get(organization=self.user)
        extra_pages = ExtraPage.objects.filter(template=self.user.organization_template)
        self.assertEquals(len(extra_pages), 2)
        self.assertTrue(extra_pages.filter(title=u'Agenda'))
        self.assertTrue(extra_pages.filter(title=u'Documentos'))
        # Probando que no se crean dos veces.
        self.user.profile.save()
        # Acá se crea un OrganizationTemplate
        extra_pages = ExtraPage.objects.filter(template=self.user.organization_template)
        self.assertEquals(len(extra_pages), 2)

    def test_extra_fields(self):
        self.user.profile.is_organization = True
        self.user.profile.save()
        template = self.user.organization_template
        template.logo = self.get_image()
        template.background_image = self.get_image()
        template.title = u'Título'
        template.sub_title = u'Bajada'
        template.org_url = u'http://ciudadanointeligente.org'
        template.facebook = u'https://www.facebook.com/ciudadanointeligente'
        template.twitter = u'https://twitter.com/ciudadanoi'
        template.instagram = u'https://www.instagram.com/fiera_feroz/'
        template.primary_color = '#FF00FF'
        template.secondary_color = '#1100FF'
        template.rss_url = 'http://blog.ciudadanointeligente.org/feed.xml'
        template.save()
        template = OrganizationTemplate.objects.get(id=self.user.organization_template.id)
        self.assertTrue(template.logo)
        self.assertTrue(template.background_image)
        self.assertTrue(template.title)
        self.assertTrue(template.sub_title)
        self.assertTrue(template.org_url)
        self.assertTrue(template.facebook)
        self.assertTrue(template.twitter)
        self.assertTrue(template.instagram)
        self.assertTrue(template.primary_color)
        self.assertTrue(template.secondary_color)
        self.assertTrue(template.rss_url)

    def test_get_absolute_url(self):
        expected_url = reverse('organization_profiles:home', kwargs={'slug': self.user.username})
        self.user.profile.is_organization = True
        self.user.profile.save()
        template = self.user.organization_template
        self.assertEquals(template.get_absolute_url(), expected_url)


class ExtraPagesPerOrganization(BackendCitizenTestCaseBase):
    def setUp(self):
        super(ExtraPagesPerOrganization, self).setUp()
        self.user = User.objects.create(username='ciudadanoi',
                                        password=PASSWORD,
                                        email='mail@mail.com')
        self.user.profile.is_organization = True
        self.user.profile.save()

    def test_attributes(self):
        extra_page = ExtraPage.objects.create(template=self.user.organization_template,
                                              title=u"Título",
                                              content=u"## Contenido")
        self.assertEquals(extra_page.template, self.user.organization_template)
        self.assertEquals(extra_page.title, u"Título")
        self.assertEquals(extra_page.content, u"## Contenido")
        self.assertTrue(extra_page.slug)
        # El regalito
        self.assertIn(u"<h2>Contenido</h2>", extra_page.content_markdown)

    def test_extra_pages_in_content(self):
        self.user.organization_template.content = u'{{#each extra_pages}}{{title}} - {{{content}}} - {{slug}}{{/each}}'
        self.user.organization_template.save()
        extra_page = ExtraPage.objects.create(template=self.user.organization_template,
                                              title=u"Título",
                                              content=u"## Contenido")

        url = reverse('organization_profiles:home', kwargs={'slug': self.user.username})
        response = self.client.get(url)
        # Esto es lo que no es unicode
        content = response.content.decode('utf-8')

        self.assertIn(extra_page.title, content)
        self.assertIn(extra_page.slug, content)
        self.assertIn(extra_page.content_markdown, content)

    def test_proposal_in_content(self):
        self.user.organization_template.content = u'{{#each proposals}} {{title}} {{/each}}'
        self.user.organization_template.save()

        popular_proposal = PopularProposal.objects.create(proposer=self.user,
                                                          area=self.arica,
                                                          data={"name": "FieraFeroz"},
                                                          title=u'This is a title',
                                                          clasification=u'education'
                                                          )

        url = reverse('organization_profiles:home', kwargs={'slug': self.user.username})
        response = self.client.get(url)
        # Esto es lo que no es unicode
        content = response.content.decode('utf-8')

        self.assertIn(popular_proposal.title, content)

    def test_sponsorhips_in_content(self):
        # Preparing sponsorships
        popular_proposal = PopularProposal.objects.create(proposer=self.fiera,
                                                          area=self.arica,
                                                          data=self.data,
                                                          title=u'This is a title'
                                                          )
        popular_proposal2 = PopularProposal.objects.create(proposer=self.fiera,
                                                           area=self.arica,
                                                           data=self.data,
                                                           title=u'Esto es un título'
                                                           )

        ProposalLike.objects.create(user=self.user,
                                    proposal=popular_proposal)

        ProposalLike.objects.create(user=self.user,
                                    proposal=popular_proposal2)

        # Hay dos organizaciones que le ponen support a esta propuesta
        # y yo quiero poder hacer que esten en alguna parte listadas

        # This is not a sponsorships
        ProposalLike.objects.create(user=self.feli,
                                    proposal=popular_proposal)

        # This is not a sponsorships

        self.user.organization_template.content = u'{{#each sponsorships }} {{title}} {{/each}}'
        self.user.organization_template.save()

        url = reverse('organization_profiles:home', kwargs={'slug': self.user.username})
        response = self.client.get(url)
        # Esto es lo que no es unicode
        content = response.content.decode('utf-8')

        self.assertIn(popular_proposal.title, content)
        self.assertIn(popular_proposal2.title, content)

    def test_get_ayuranos(self):
        first_candidate = Candidate.objects.first()
        popular_proposal = PopularProposal.objects.create(proposer=self.user,
                                                          area=self.arica,
                                                          data={"name": "FieraFeroz"},
                                                          title=u'This is a title',
                                                          clasification=u'education'
                                                          )

        url = reverse('organization_profiles:ayuranos', kwargs={'slug': self.user.username})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'organization_profiles/ayuranos.html')
        self.assertIn(first_candidate, response.context['candidates'])

    @override_settings(PRIORITY_CANDIDATES=[2,])
    def test_get_priority_candidates(self):
        first_candidate = Candidate.objects.get(id=2)
        popular_proposal = PopularProposal.objects.create(proposer=self.user,
                                                          area=self.arica,
                                                          data={"name": "FieraFeroz"},
                                                          title=u'This is a title',
                                                          clasification=u'education'
                                                          )

        url = reverse('organization_profiles:ayuranos', kwargs={'slug': self.user.username})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'organization_profiles/ayuranos.html')
        self.assertIn(first_candidate, response.context['candidates'])
        self.assertEquals(len(response.context['candidates']), 1)


class OrganizationListView(BackendCitizenTestCaseBase):
    def setUp(self):
        super(OrganizationListView, self).setUp()
        self.user = User.objects.create(username='ciudadanoi',
                                        password=PASSWORD,
                                        email='mail@mail.com')
        self.user.profile.is_organization = True
        self.user.profile.save()

    def test_get_list(self):
        url = reverse('organization_profiles:index')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'organization_profiles/index.html')
