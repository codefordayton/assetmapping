from django.core.management.base import BaseCommand
from django.utils.text import slugify
from assets.models import Category, Asset


CATEGORIES = [
    {'name': 'Community Orgs & Nonprofits', 'slug': 'community', 'icon': 'users', 'color': 'purple',
     'description': 'Neighborhood associations, nonprofits, mutual aid, faith communities'},
    {'name': 'Green Space & Parks', 'slug': 'greenspace', 'icon': 'tree', 'color': 'green',
     'description': 'Parks, community gardens, urban farms, trails, and outdoor spaces'},
    {'name': 'Small Businesses', 'slug': 'business', 'icon': 'store', 'color': 'orange',
     'description': 'Local shops, restaurants, and services with community value'},
    {'name': 'Skills & People', 'slug': 'skills', 'icon': 'user', 'color': 'blue',
     'description': 'Neighbors offering skills, knowledge, or services to the community'},
]

ASSETS = [
    # Community Orgs
    {
        'name': 'Old North Dayton Neighborhood Association',
        'category': 'community',
        'description': 'The primary resident organization for Old North Dayton. Holds monthly meetings, organizes clean-ups, and advocates for neighborhood improvements.',
        'address': '1501 Germantown St, Dayton, OH 45408',
        'latitude': 39.7738, 'longitude': -84.1701,
        'phone': '(937) 555-0101',
        'hours': 'Meetings: 2nd Tuesday of each month, 6pm',
        'tags': 'neighborhood, meetings, advocacy',
        'verified': True,
    },
    {
        'name': 'St. Peter Catholic Church Food Pantry',
        'category': 'community',
        'description': 'Weekly food pantry open to all Dayton residents. No proof of residency required. Provides shelf-stable groceries, fresh produce when available.',
        'address': '1314 E. Third St, Dayton, OH 45403',
        'latitude': 39.7695, 'longitude': -84.1755,
        'phone': '(937) 228-2013',
        'hours': 'Saturdays 9am–12pm',
        'tags': 'food, pantry, free, hunger',
        'verified': True,
    },
    {
        'name': 'Old North Dayton Mutual Aid Network',
        'category': 'community',
        'description': 'A neighbor-to-neighbor support network. Request or offer help with groceries, childcare, transportation, home repairs, and more.',
        'address': 'Old North Dayton, Dayton, OH',
        'latitude': 39.7720, 'longitude': -84.1720,
        'phone': '',
        'website': 'https://example.org/ondmutualaid',
        'hours': 'Requests accepted anytime via form',
        'tags': 'mutual aid, support, neighbors, free',
        'verified': False,
    },
    {
        'name': 'Dayton Urban Garden Network — OND Chapter',
        'category': 'community',
        'description': 'Local chapter of the citywide urban garden network. Runs workshops on composting, seed saving, and urban farming for Old North residents.',
        'address': '1720 Wayne Ave, Dayton, OH 45410',
        'latitude': 39.7748, 'longitude': -84.1690,
        'phone': '(937) 555-0188',
        'hours': 'Workshop schedule posted monthly',
        'tags': 'gardens, workshops, composting, food',
        'verified': True,
    },
    {
        'name': 'Living Water Community Church',
        'category': 'community',
        'description': 'A neighborhood church hosting after-school tutoring, a summer lunch program for youth, and seasonal community dinners.',
        'address': '1601 Gettysburg Ave, Dayton, OH 45408',
        'latitude': 39.7730, 'longitude': -84.1680,
        'phone': '(937) 555-0244',
        'hours': 'Sun services 10am; Tutoring: Mon/Wed 3:30–5:30pm',
        'tags': 'church, tutoring, youth, lunch program',
        'verified': True,
    },

    # Green Space & Parks
    {
        'name': 'Westwood Park',
        'category': 'greenspace',
        'description': 'A neighborhood park with a playground, basketball courts, and open green space. Popular with families and youth sports leagues.',
        'address': '1800 N. James H. McGee Blvd, Dayton, OH 45417',
        'latitude': 39.7760, 'longitude': -84.1745,
        'phone': '',
        'hours': 'Dawn to dusk',
        'tags': 'park, playground, basketball, families',
        'verified': True,
    },
    {
        'name': 'Old North Community Garden',
        'category': 'greenspace',
        'description': 'A shared community garden with 24 raised beds available to rent. Rainwater collection system on site. Managed by the Dayton Urban Garden Network.',
        'address': '1412 Leo St, Dayton, OH 45408',
        'latitude': 39.7715, 'longitude': -84.1735,
        'phone': '(937) 555-0188',
        'hours': 'Open to members year-round',
        'tags': 'garden, raised beds, urban agriculture, food',
        'verified': True,
    },
    {
        'name': 'Findlay Street Pocket Park',
        'category': 'greenspace',
        'description': 'A small pocket park with native plantings, a rain garden, and two benches. Designed and maintained by OND residents. Great spot for a quiet break.',
        'address': 'Findlay St & Bainbridge St, Dayton, OH 45408',
        'latitude': 39.7702, 'longitude': -84.1708,
        'hours': 'Always open',
        'tags': 'pocket park, native plants, rain garden',
        'verified': False,
    },
    {
        'name': 'Wegerzyn Gardens MetroPark — North Trail',
        'category': 'greenspace',
        'description': 'Access point to the Stillwater River trail system. Paved path connects to the larger MetroPark trail network. Dog-friendly, ADA accessible.',
        'address': '1301 E. Siebenthaler Ave, Dayton, OH 45414',
        'latitude': 39.7795, 'longitude': -84.1688,
        'phone': '(937) 277-4374',
        'website': 'https://www.metroparks.org',
        'hours': '6:30am–10pm daily',
        'tags': 'trail, river, walking, dogs, accessible',
        'verified': True,
    },

    # Small Businesses
    {
        'name': 'Old North Barber & Style',
        'category': 'business',
        'description': 'Family-owned barbershop serving Old North Dayton for over 20 years. Walk-ins welcome. Known for fades, line-ups, and kids\' cuts.',
        'address': '1523 Wayne Ave, Dayton, OH 45410',
        'latitude': 39.7708, 'longitude': -84.1722,
        'phone': '(937) 555-0312',
        'hours': 'Tue–Sat 9am–6pm',
        'tags': 'barbershop, haircuts, family, local',
        'verified': True,
    },
    {
        'name': 'Germantown Street Deli & Market',
        'category': 'business',
        'description': 'A neighborhood cornerstore and deli serving hot breakfast and lunch. Stocked with produce, dairy, and pantry staples. Accepts EBT/SNAP.',
        'address': '1488 Germantown St, Dayton, OH 45408',
        'latitude': 39.7733, 'longitude': -84.1712,
        'phone': '(937) 555-0399',
        'hours': 'Mon–Sat 7am–7pm; Sun 8am–4pm',
        'tags': 'grocery, deli, EBT, SNAP, food access',
        'verified': True,
    },
    {
        'name': 'Bainbridge Fix-It Shop',
        'category': 'business',
        'description': "General repair shop: small appliances, bikes, lawnmowers. If it's broken, they'll try to fix it. Competitive rates; seniors get 10% off.",
        'address': '1609 Bainbridge St, Dayton, OH 45408',
        'latitude': 39.7741, 'longitude': -84.1732,
        'phone': '(937) 555-0427',
        'hours': 'Mon–Fri 10am–5pm',
        'tags': 'repair, appliances, bikes, seniors',
        'verified': False,
    },

    # Skills & People
    {
        'name': 'Maria G. — Spanish/English Tutoring',
        'category': 'skills',
        'description': 'Lifelong OND resident offering Spanish language tutoring for adults and conversational English lessons for Spanish speakers. Sliding-scale rates.',
        'address': 'Old North Dayton (exact location by appointment)',
        'latitude': 39.7725, 'longitude': -84.1742,
        'phone': '(937) 555-0511',
        'hours': 'Evenings and weekends, by appointment',
        'tags': 'tutoring, Spanish, English, language, adults',
        'submitted_by': 'Maria G.',
        'verified': True,
    },
    {
        'name': 'James T. — Home Repair & Plumbing',
        'category': 'skills',
        'description': 'Retired plumber offering free or low-cost help with minor plumbing, drywall, and carpentry for elderly or low-income neighbors. Call first.',
        'address': 'Old North Dayton (contact for location)',
        'latitude': 39.7718, 'longitude': -84.1758,
        'phone': '(937) 555-0588',
        'hours': 'Available weekends',
        'tags': 'plumbing, repairs, carpentry, free, seniors, low-income',
        'submitted_by': 'James T.',
        'verified': True,
    },
    {
        'name': 'OND Tech Help — Free Device Support',
        'category': 'skills',
        'description': 'Volunteers available to help neighbors with smartphones, tablets, and computers. Password resets, app setup, email, video calls. No charge.',
        'address': '1601 Gettysburg Ave, Dayton, OH 45408',
        'latitude': 39.7731, 'longitude': -84.1675,
        'phone': '(937) 555-0622',
        'hours': 'Thursdays 5–7pm at Living Water Church',
        'tags': 'tech help, digital literacy, free, seniors, computers',
        'verified': True,
    },
]


class Command(BaseCommand):
    help = 'Seed Old North Dayton demo data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding categories...')
        cat_map = {}
        for c in CATEGORIES:
            obj, created = Category.objects.update_or_create(
                slug=c['slug'],
                defaults=c,
            )
            cat_map[c['slug']] = obj
            self.stdout.write(f'  {"Created" if created else "Updated"}: {obj.name}')

        self.stdout.write('Seeding assets...')
        for a in ASSETS:
            cat_slug = a.pop('category')
            a['category'] = cat_map[cat_slug]
            a['status'] = 'active'
            obj, created = Asset.objects.update_or_create(
                name=a['name'],
                defaults=a,
            )
            self.stdout.write(f'  {"Created" if created else "Updated"}: {obj.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {Category.objects.count()} categories, {Asset.objects.count()} assets.'
        ))
