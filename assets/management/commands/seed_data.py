from django.core.management.base import BaseCommand
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

# Greenwich Village is on the west side of Dayton, centered ~39.793, -84.262
# Precincts 16D and 16E
ASSETS = [
    # Community Orgs
    {
        'name': 'Greenwich Village Neighborhood Association',
        'category': 'community',
        'description': 'The primary resident organization for Greenwich Village. Holds monthly meetings, coordinates neighborhood clean-ups, and works with the City of Dayton on local improvements.',
        'address': '3400 W. Third St, Dayton, OH 45417',
        'latitude': 39.7930, 'longitude': -84.2620,
        'phone': '(937) 555-0101',
        'hours': 'Meetings: 2nd Tuesday of each month, 6:30pm',
        'tags': 'neighborhood, meetings, advocacy',
        'verified': True,
    },
    {
        'name': 'DUHR Movement — Greenwich Village',
        'category': 'community',
        'description': 'Local organizing hub for the DUHR Movement, focused on housing justice, voter engagement, and community development in Greenwich Village and surrounding west Dayton neighborhoods.',
        'address': 'Greenwich Village, Dayton, OH 45417',
        'latitude': 39.7938, 'longitude': -84.2608,
        'phone': '',
        'website': 'https://duhrmovement.org',
        'hours': 'By appointment',
        'tags': 'housing, organizing, voting, west dayton',
        'verified': True,
    },
    {
        'name': 'New Covenant Community Church Food Pantry',
        'category': 'community',
        'description': 'Weekly food pantry serving Greenwich Village and west Dayton residents. No proof of residency required. Fresh produce available in season.',
        'address': '3501 Salem Ave, Dayton, OH 45406',
        'latitude': 39.7955, 'longitude': -84.2572,
        'phone': '(937) 555-0213',
        'hours': 'Thursdays 10am–1pm',
        'tags': 'food, pantry, free, hunger',
        'verified': True,
    },
    {
        'name': 'West Dayton Mutual Aid Network',
        'category': 'community',
        'description': 'Neighbor-to-neighbor support covering Greenwich Village and surrounding precincts. Request or offer help with groceries, rides, childcare, and home repairs.',
        'address': 'Greenwich Village, Dayton, OH 45417',
        'latitude': 39.7922, 'longitude': -84.2635,
        'website': 'https://example.org/westdaytonmutualaid',
        'hours': 'Requests accepted anytime via online form',
        'tags': 'mutual aid, support, free, neighbors',
        'verified': False,
    },
    {
        'name': 'Salem Avenue Baptist Church',
        'category': 'community',
        'description': 'Established community anchor in Greenwich Village running a summer youth program, back-to-school supply drive, and monthly senior luncheons.',
        'address': '3320 Salem Ave, Dayton, OH 45406',
        'latitude': 39.7948, 'longitude': -84.2580,
        'phone': '(937) 555-0244',
        'hours': 'Sun services 10:30am; Youth program: Tue/Thu 3–5pm',
        'tags': 'church, youth, seniors, community',
        'verified': True,
    },

    # Green Space & Parks
    {
        'name': 'Westwood Park',
        'category': 'greenspace',
        'description': 'Neighborhood park with a playground, basketball court, and open green space. Managed by Dayton Metro Parks. Popular with families in precincts 16D and 16E.',
        'address': '3600 W. Third St, Dayton, OH 45417',
        'latitude': 39.7918, 'longitude': -84.2658,
        'hours': 'Dawn to dusk',
        'tags': 'park, playground, basketball, families',
        'verified': True,
    },
    {
        'name': 'Greenwich Village Community Garden',
        'category': 'greenspace',
        'description': 'A shared raised-bed garden on a reclaimed vacant lot. Twenty plots available to neighborhood residents on a first-come basis. Managed by volunteers.',
        'address': 'W. Third St & Gettysburg Ave, Dayton, OH 45417',
        'latitude': 39.7927, 'longitude': -84.2643,
        'hours': 'Open to members year-round',
        'tags': 'garden, raised beds, food, urban agriculture',
        'verified': True,
    },
    {
        'name': 'Salem Ave Greenway Trail Access',
        'category': 'greenspace',
        'description': 'Access point to the Salem Avenue greenway trail corridor. Connects to the Great Miami River trail system. Paved, ADA accessible, dog-friendly.',
        'address': 'Salem Ave & Olive Rd, Dayton, OH 45406',
        'latitude': 39.7962, 'longitude': -84.2561,
        'hours': 'Always open',
        'tags': 'trail, walking, biking, accessible, dogs',
        'verified': True,
    },
    {
        'name': 'Gettysburg Pocket Park',
        'category': 'greenspace',
        'description': 'A small resident-maintained pocket park with native plantings, two benches, and a Little Free Library. Maintained by the Greenwich Village Neighborhood Association.',
        'address': 'Gettysburg Ave & Horace St, Dayton, OH 45417',
        'latitude': 39.7910, 'longitude': -84.2628,
        'hours': 'Always open',
        'tags': 'pocket park, native plants, little free library',
        'verified': False,
    },

    # Small Businesses
    {
        'name': 'Salem Ave Barber Shop',
        'category': 'business',
        'description': 'Family-run barbershop on Salem Ave serving Greenwich Village for 15+ years. Walk-ins welcome. Known for precision cuts and a welcoming atmosphere.',
        'address': '3344 Salem Ave, Dayton, OH 45406',
        'latitude': 39.7950, 'longitude': -84.2577,
        'phone': '(937) 555-0312',
        'hours': 'Tue–Sat 9am–6pm',
        'tags': 'barbershop, haircuts, family, local',
        'verified': True,
    },
    {
        'name': 'West Third Street Market',
        'category': 'business',
        'description': 'Corner grocery and deli serving the Greenwich Village neighborhood. Hot breakfast, fresh produce, and pantry staples. Accepts EBT/SNAP.',
        'address': '3410 W. Third St, Dayton, OH 45417',
        'latitude': 39.7929, 'longitude': -84.2617,
        'phone': '(937) 555-0399',
        'hours': 'Mon–Sat 7am–8pm; Sun 8am–5pm',
        'tags': 'grocery, deli, EBT, SNAP, food access',
        'verified': True,
    },
    {
        'name': "Horace's Fix-It & Hardware",
        'category': 'business',
        'description': 'Small hardware and repair shop. Stock of basic home repair supplies plus same-day repairs on small appliances. Senior discount Wednesdays.',
        'address': '3388 W. Third St, Dayton, OH 45417',
        'latitude': 39.7932, 'longitude': -84.2611,
        'phone': '(937) 555-0427',
        'hours': 'Mon–Fri 9am–5pm; Sat 9am–2pm',
        'tags': 'hardware, repair, appliances, seniors',
        'verified': False,
    },

    # Skills & People
    {
        'name': 'Rosa M. — GED & Adult Literacy Tutoring',
        'category': 'skills',
        'description': 'Longtime Greenwich Village resident offering free GED prep and adult reading tutoring. Meets at the Salem Ave library branch or by arrangement.',
        'address': 'Greenwich Village (by appointment)',
        'latitude': 39.7935, 'longitude': -84.2630,
        'phone': '(937) 555-0511',
        'hours': 'Weekday evenings and Saturday mornings',
        'tags': 'GED, tutoring, literacy, adults, free',
        'submitted_by': 'Rosa M.',
        'verified': True,
    },
    {
        'name': 'DeShawn T. — Electrical & General Home Repair',
        'category': 'skills',
        'description': 'Licensed electrician offering free consultations and reduced-rate repairs for elderly and low-income neighbors in Greenwich Village. Call ahead.',
        'address': 'Greenwich Village (contact for location)',
        'latitude': 39.7920, 'longitude': -84.2648,
        'phone': '(937) 555-0588',
        'hours': 'Available weekends',
        'tags': 'electrical, repairs, free consultation, seniors, low-income',
        'submitted_by': 'DeShawn T.',
        'verified': True,
    },
    {
        'name': 'Greenwich Village Tech Help',
        'category': 'skills',
        'description': 'Volunteer-run tech support drop-in. Help with smartphones, tablets, email, video calls, and online benefits portals. No appointment needed. No charge.',
        'address': '3320 Salem Ave, Dayton, OH 45406',
        'latitude': 39.7948, 'longitude': -84.2582,
        'hours': 'Wednesdays 5–7pm at Salem Ave Baptist Church',
        'tags': 'tech help, digital literacy, free, seniors, computers',
        'verified': True,
    },
]


class Command(BaseCommand):
    help = 'Seed Greenwich Village demo data'

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
