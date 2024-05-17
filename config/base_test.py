from utils.assertions import Assertions
from services.booking.endpoints import Endpoints as booker
from services.auth.endpoints import Endpoints as auth
from services.ping.endpoints import Endpoints as ping
from services.booking.endpoints import QueryParams
from services.booking.schemas import XSDSchemas
from services.booking.schemas import CreateBookingSchema
from services.booking.schemas import GetBookingSchema
from services.booking.schemas import GetBookingIds
from services.booking.payloads import generate_body_booking
from services.auth.payloads import generate_body_auth
from services.auth.schemas import AuthTokenSchema


class BaseTest:

    def setup_method(self):
        # assertions
        self.check = Assertions()

        # endpoints
        self.ep_booker = booker()
        self.ep_auth = auth()
        self.ep_ping = ping()
        self.query = QueryParams()

        # schemas
        self.xsd_schema = XSDSchemas()
        self.create_schema = CreateBookingSchema
        self.get_schema = GetBookingSchema
        self.get_ids_schema = GetBookingIds
        self.auth_token_schema = AuthTokenSchema

        # payloads
        self.generate_body_booking = generate_body_booking
        self.generate_body_auth = generate_body_auth
