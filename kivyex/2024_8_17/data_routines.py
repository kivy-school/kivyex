# https://github.com/kivy/kivy/issues/8802#issuecomment-2295245329

from sqlite3 import connect


class DataRtns:

    db = None
    cursor = None

    @staticmethod
    def validate_database(interface):

        # Create a Connection to Data, create Database if it doesn't exist

        try:
            DataRtns.db = connect("shipping.db")
            DataRtns.cursor = DataRtns.db.cursor()
        except Exception as err:
            interface.err_flg = True
            interface.ids.status_indicator.text = "Connection Failed: " + str(err)

        if interface.err_flg == False:
            interface.ids.status_indicator.text = "Validated Database"

    @staticmethod
    def check_tables(interface):

        # Validate Tables, create if they don't exist

        files = ["addresses", "schedule", "addr_types", "prefixes", "suffixes", "service_types"]

        for file in files:

            if file == "addresses":

                try:

                    DataRtns.cursor.execute("CREATE TABLE IF NOT EXISTS addresses(id INTEGER PRIMARY KEY, "
                                            "street_no INTEGER NOT NULL, street_name TEXT NOT NULL, "
                                            "street_suffix TEXT NOT NULL, street_prefix TEXT, "
                                            "unit_suite TEXT, city TEXT NOT NULL, province TEXT NOT NULL, "
                                            "postal TEXT NOT NULL, landline TEXT, cell TEXT, "
                                            "address_type TEXT NOT NULL, map TEXT, photo TEXT, "
                                            "directions TEXT, location_notes TEXT, "
                                            "cancellations INTEGER DEFAULT 0, failures INTEGER DEFAULT 0, "
                                            "completed INTEGER DEFAULT 0, status TEXT, "
                                            "status_description TEXT, time_stamp TEXT)")

                except Exception as err:
                    DataRtns.db.close()
                    interface.err_flg = True
                    interface.ids.status_indicator.text = "Problem with addresses: " + str(err)
                    break

            elif file == "schedule":

                try:

                    DataRtns.cursor.execute("CREATE TABLE IF NOT EXISTS schedule(rowid INTEGER PRIMARY KEY, "
                                            "addrid INTEGER NOT NULL, address TEXT NOT NULL, "
                                            "city TEXT NOT NULL, type TEXT NOT NULL, "
                                            "notes TEXT, status TEXT, time_stamp TEXT)")

                except Exception as err:
                    DataRtns.db.close()
                    interface.err_flg = True
                    interface.ids.status_indicator.text = "Problem with schedule: " + str(err)
                    break

            elif file == "addr_types":

                try:

                    DataRtns.cursor.execute("CREATE TABLE IF NOT EXISTS addr_types(id INTEGER PRIMARY KEY, "
                                            "type TEXT NOT NULL, multi_unit INTEGER DEFAULT 0)")

                except Exception as err:
                    DataRtns.db.close()
                    interface.err_flg = True
                    interface.ids.status_indicator.text = "Problem with addr_types: " + str(err)
                    break

            elif file == "prefixes":

                try:

                    DataRtns.cursor.execute("CREATE TABLE IF NOT EXISTS prefixes(id INTEGER PRIMARY KEY, "
                                            "street_direction TEXT NOT NULL, abbreviation TEXT NOT NULL)")

                except Exception as err:
                    DataRtns.db.close()
                    interface.err_flg = True
                    interface.ids.status_indicator.text = "Problem with prefixes: " + str(err)
                    break

            elif file == "suffixes":

                try:

                    DataRtns.cursor.execute("CREATE TABLE IF NOT EXISTS suffixes(id INTEGER PRIMARY KEY, "
                                            "street_type TEXT NOT NULL, abbreviation TEXT NOT NULL)")

                except Exception as err:
                    DataRtns.db.close()
                    interface.err_flg = True
                    interface.ids.status_indicator.text = "Problem with suffixes: " + str(err)
                    break

            elif file == "service_types":

                try:

                    DataRtns.cursor.execute("CREATE TABLE IF NOT EXISTS service_types(id INTEGER PRIMARY KEY, "
                                            "type TEXT NOT NULL)")

                except Exception as err:
                    DataRtns.db.close()
                    interface.err_flg = True
                    interface.ids.status_indicator.text = "Problem with service_types: " + str(err)
                    break

        if interface.err_flg == False:
            interface.ids.status_indicator.text = "Checked Tables"

    @staticmethod
    def check_defaults(interface):

        # Validate Maintenance Files, should contain default values used in the application

        result = []
        chk_result = []

        files = ["addr_types", "prefixes", "suffixes", "service_types"]

        for file in files:

            if interface.err_flg:
                break

            if file == "addr_types":

                # Address Type Defaults

                values = [("Apartment Building", 1),
                          ("Assisted Living Building", 1),
                          ("Basement Apartment", 0),
                          ("Business (detached)", 0),
                          ("Condominium", 1),
                          ("Flat", 0),
                          ("House (detached)", 0),
                          ("House (linked)", 0),
                          ("Loft", 0),
                          ("Maisonette", 1),
                          ("Office Building", 1),
                          ("Retirement Home", 1),
                          ("Row House", 1),
                          ("Seniors Residence", 1),
                          ("Store Front", 0),
                          ("Plaza", 1),
                          ("Mall", 1),
                          ("Townhouse", 1),
                          ("Townhouse (no unit)", 0),
                          ("Trailer Park", 0)]

                # Access addr_types

                try:
                    sql = f"SELECT * from {file}"
                    DataRtns.cursor.execute(sql)
                    result = DataRtns.cursor.fetchall()
                except Exception as err:
                    DataRtns.db.close()
                    interface.err_flg = True
                    interface.ids.status_indicator.text = "Problem accessing addr_types: " + str(err)
                    break

                # Check Records

                if len(result) > 0:

                    for value_items in values:

                        try:
                            sql = f"SELECT * from {file} where type = '{value_items[0]}'"
                            DataRtns.cursor.execute(sql)
                            chk_result = DataRtns.cursor.fetchall()
                        except Exception as err:
                            DataRtns.db.close()
                            interface.err_flg = True
                            interface.ids.status_indicator.text = f"Problem accessing {file}: " + str(err)
                            break

                        if len(chk_result) == 0:

                            desc = value_items[0]
                            munit = value_items[1]

                            try:
                                sql = f"INSERT INTO {file} (type, multi_unit) VALUES (?, ?)"
                                vals = (f"{desc}", f"{munit}")
                                DataRtns.cursor.execute(sql, vals)
                                DataRtns.db.commit()
                            except Exception as err:
                                DataRtns.db.close()
                                interface.err_flg = True
                                interface.ids.status_indicator.text = f"Problem update {file}: " + str(err)
                                break

                else:

                    # Add Records

                    for value_items in values:

                        desc = value_items[0]
                        munit = value_items[1]

                        try:
                            sql = f"INSERT INTO {file} (type, multi_unit) VALUES (?, ?)"
                            vals = (f"{desc}", f"{munit}")
                            DataRtns.cursor.execute(sql, vals)
                            DataRtns.db.commit()
                        except Exception as err:
                            DataRtns.db.close()
                            interface.err_flg = True
                            interface.ids.status_indicator.text = f"Problem updating {file}: " + str(err)
                            break

            elif file == "prefixes":

                # Street Direction Defaults

                values = [("East", "E"),
                          ("North", "N"),
                          ("Northeast", "NE"),
                          ("Northwest", "NW"),
                          ("South", "S"),
                          ("Southeast", "SE"),
                          ("Southwest", "SW"),
                          ("West", "W")]

                # Access prefixes

                try:
                    sql = f"SELECT * from {file}"
                    DataRtns.cursor.execute(sql)
                    result = DataRtns.cursor.fetchall()
                except Exception as err:
                    DataRtns.db.close()
                    interface.err_flg = True
                    interface.ids.status_indicator.text = "Problem accessing prefixes: " + str(err)
                    break

                # Check Records

                if len(result) > 0:

                    for value_items in values:

                        try:
                            sql = f"SELECT * from {file} where street_direction = '{value_items[0]}'"
                            DataRtns.cursor.execute(sql)
                            chk_result = DataRtns.cursor.fetchall()
                        except Exception as err:
                            DataRtns.db.close()
                            interface.err_flg = True
                            interface.ids.status_indicator.text = f"Problem accessing {file}: " + str(err)
                            break

                        if len(chk_result) == 0:

                            direction = value_items[0]
                            short_desc = value_items[1]

                            try:
                                sql = f"INSERT INTO {file} (street_direction, abbreviation) VALUES (?, ?)"
                                vals = (f"{direction}", f"{short_desc}")
                                DataRtns.cursor.execute(sql, vals)
                                DataRtns.db.commit()
                            except Exception as err:
                                DataRtns.db.close()
                                interface.err_flg = True
                                interface.ids.status_indicator.text = f"Problem updating {file}: " + str(err)
                                break

                else:

                    # Add Records

                    for value_items in values:

                        direction = value_items[0]
                        short_desc = value_items[1]

                        try:
                            sql = f"INSERT INTO {file} (street_direction, abbreviation) VALUES (?, ?)"
                            vals = (f"{direction}", f"{short_desc}")
                            DataRtns.cursor.execute(sql, vals)
                            DataRtns.db.commit()
                        except Exception as err:
                            DataRtns.db.close()
                            interface.err_flg = True
                            interface.ids.status_indicator.text = f"Problem updating {file}: " + str(err)
                            break

            elif file == "suffixes":

                # Street Type Defaults

                values = [("Abbey", "Abbey"),
                          ("Acres", "Acres"),
                          ("Alley", "Alley"),
                          ("Avenue", "Ave"),
                          ("Bay", "Bay"),
                          ("Beach", "Beach"),
                          ("Boulevard", "Blvd"),
                          ("Bye-pass", "Bypass"),
                          ("Campus", "Campus"),
                          ("Centre", "Ctr"),
                          ("Circle", "Cir"),
                          ("Concession", "Conc"),
                          ("Corners", "Crnrs"),
                          ("Court", "Crt"),
                          ("Cove", "Cove"),
                          ("Crescent", "Cres"),
                          ("Crossing", "Cross"),
                          ("Downs", "Downs"),
                          ("Drive", "Dr"),
                          ("Esplanade", "Espl"),
                          ("Expressway", "Expy"),
                          ("Extension", "Exten"),
                          ("Freeway", "Fwy"),
                          ("Glen", "Glen"),
                          ("Grove", "Grove"),
                          ("Harbour", "Harbr"),
                          ("Heights", "Hts"),
                          ("Highway", "Hwy"),
                          ("Hill", "Hill"),
                          ("Key", "Key"),
                          ("Landing", "Landing"),
                          ("Lane", "Lane"),
                          ("Line", "Line"),
                          ("Mall", "Mall"),
                          ("Manor", "Manor"),
                          ("Meadows", "Meadows"),
                          ("Mews", "Mews"),
                          ("Mountain", "Mtn"),
                          ("Orchard", "Orch"),
                          ("Park", "Pk"),
                          ("Parkway", "Pky"),
                          ("Place", "Pl"),
                          ("Plaza", "Plaza"),
                          ("Promenade", "Prom"),
                          ("Ridge", "Ridge"),
                          ("Road", "Rd"),
                          ("Route", "Rte"),
                          ("Square", "Sq"),
                          ("Street", "St"),
                          ("Terrace", "Terr"),
                          ("Towers", "Towers"),
                          ("Townline", "Tline"),
                          ("Trail", "Trail"),
                          ("View", "View"),
                          ("Village", "Vilge"),
                          ("Way", "Way")]

                # Access Street Types

                try:
                    sql = f"SELECT * from {file}"
                    DataRtns.cursor.execute(sql)
                    result = DataRtns.cursor.fetchall()
                except Exception as err:
                    DataRtns.db.close()
                    interface.err_flg = True
                    interface.ids.status_indicator.text = f"Problem accessing suffixes: " + str(err)
                    break

                # Check Records

                if len(result) > 0:

                    for value_items in values:

                        try:
                            sql = f"SELECT * from {file} where street_type = '{value_items[0]}'"
                            DataRtns.cursor.execute(sql)
                            chk_result = DataRtns.cursor.fetchall()
                        except Exception as err:
                            DataRtns.db.close()
                            interface.err_flg = True
                            interface.ids.status_indicator.text = f"Problem accessing {file}: " + str(err)
                            break

                        if len(chk_result) == 0:

                            strt_type = value_items[0]
                            short_desc = value_items[1]

                            try:
                                sql = f"INSERT INTO {file} (street_type, abbreviation) VALUES (?, ?)"
                                vals = (f"{strt_type}", f"{short_desc}")
                                DataRtns.cursor.execute(sql, vals)
                                DataRtns.db.commit()
                            except Exception as err:
                                DataRtns.db.close()
                                interface.err_flg = True
                                interface.ids.status_indicator = f"Problem updateing {file}: " + str(err)
                                break

                else:

                    # Add Records

                    for value_items in values:

                        strt_type = value_items[0]
                        short_desc = value_items[1]

                        try:
                            sql = f"INSERT INTO {file} (street_type, abbreviation) VALUES (?, ?)"
                            vals = (f"{strt_type}", f"{short_desc}")
                            DataRtns.cursor.execute(sql, vals)
                            DataRtns.db.commit()
                        except Exception as err:
                            DataRtns.db.close()
                            interface.err_flg = True
                            interface.ids.status_indicator.text = f"Problem updating {file}: " + str(err)
                            break

            elif file == "service_types":

                # Service Type Defaults

                values = ["Delivery",
                          "Desk Work",
                          "Dog Walking",
                          "Gardening",
                          "Lawn Mow",
                          "Leaf Raking",
                          "Other",
                          "Pet Sitting",
                          "Put Garbage Out",
                          "Snow Shoveling",
                          "Trash Removal"]

                # Access service_types

                try:
                    sql = f"SELECT * from {file}"
                    DataRtns.cursor.execute(sql)
                    result = DataRtns.cursor.fetchall()
                except Exception as err:
                    DataRtns.db.close()
                    interface.err_flg = True
                    interface.ids.status_indicator.text = f"Problem accessing service_types: " + str(err)
                    break

                # Check Records

                if len(result) > 0:

                    for value_items in values:

                        try:
                            sql = f"SELECT * from {file} where type = '{value_items[0]}'"
                            DataRtns.cursor.execute(sql)
                            chk_result = DataRtns.cursor.fetchall()
                        except Exception as err:
                            DataRtns.db.close()
                            interface.err_flg = True
                            interface.ids.status_indicator.text = f"Problem accessing {file}: " + str(err)
                            break

                        if len(chk_result) == 0:

                            service = value_items[0]

                            try:
                                sql = f"INSERT INTO {file} (type) VALUES (?)"
                                vals = f"{service}"
                                DataRtns.cursor.execute(sql, vals)
                                DataRtns.db.commit()
                            except Exception as err:
                                DataRtns.db.close()
                                interface.err_flg = True
                                interface.ids.status_indicator.text = f"Problem updating {file}: " + str(err)
                                break

                else:

                    # Add Records

                    for value_items in values:

                        service = value_items[0]

                        try:
                            sql = f"INSERT INTO {file} (type) VALUES (?)"
                            vals = f"{service}"
                            DataRtns.cursor.execute(sql, vals)
                            DataRtns.db.commit()
                        except Exception as err:
                            DataRtns.db.close()
                            interface.err_flg = True
                            interface.ids.status_indicator.text = f"Problem updating {file}: " + str(err)
                            break

        if interface.err_flg == False:

            DataRtns.cursor.close()
            DataRtns.db.close()

            interface.ids.status_indicator.text = "Checked Defaults"
