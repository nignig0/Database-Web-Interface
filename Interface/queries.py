def getLast30DaysQueries(db_cursor):
    db_cursor.execute("""
    SELECT 
    HR.Request_ID,
    RS.StatusName,
    HR.Symptoms,
    HR.Created_At,
    DS.FirstName AS StudentFirstName,
    DS.LastName AS StudentLastName,
    DATEDIFF(CURRENT_DATE, HR.Created_At) AS Days_Ago
FROM 
    Health_Request HR
INNER JOIN 
    HealthRequest_Status_Relation HRS ON HR.Request_ID = HRS.Request_ID
INNER JOIN
	RequestStatus RS ON RS.StatusID = HRS.StatusID
INNER JOIN 
    HealthRequest_Student_Course_Relation RSR ON HR.Request_ID = RSR.Request_ID
INNER JOIN 
    Student DS ON RSR.StudentID = DS.StudentID
WHERE 
    HR.Created_At >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
GROUP BY 
    HR.Request_ID, RS.StatusName, HR.Symptoms, HR.Created_At, DS.FirstName, DS.LastName
ORDER BY 
    HR.Created_At DESC;    
    """)
    table_rows = db_cursor.fetchall()
    return table_rows


def findStudentsMultipleHealthRequests(db_cursor):
    db_cursor.execute("""
    with StudentsWithRequests as (
    select 
        rsr.StudentID
    from 
        HealthRequest_Student_Course_Relation rsr
    group by
        rsr.StudentID
    having
        COUNT(rsr.Request_ID) >= 1
)

select 
    a.FirstName, 
    a.LastName, 
    a.Email, 
    a.PhoneNumber, 
    r.Request_ID, 
    s.StatusName
from 
    Student a
inner join 
    HealthRequest_Student_Course_Relation rsr on a.StudentID = rsr.StudentID 
inner join 
    Health_Request r on rsr.Request_ID = r.Request_ID
inner join  
    HealthRequest_Status_Relation hsr on hsr.Request_ID = r.Request_ID
inner join 
    RequestStatus s on s.StatusID = hsr.StatusID
inner join 
    StudentsWithRequests swr on a.StudentID = swr.StudentID;
    """)
    return db_cursor.fetchall()


def getNumberOfRequestsApprovedByHP(db_cursor, personnelID): 
    #gets the number of requests approved by a certain health personnel
    db_cursor.execute(f"""
    SELECT hp.HP_ID, concat(hp.FirstName, ' ', hp.LastName) as Name, COUNT(a.HP_ID) AS approved_requests
    FROM Health_Personnel hp
    LEFT OUTER JOIN Approved_By a ON hp.HP_ID = a.HP_ID
    WHERE hp.HP_ID = '{personnelID}';

    """)
    return db_cursor.fetchall()

def countRequestsInADay(db_cursor, dateString):
    #counts the number of requests in a day
    db_cursor.execute(f"""
    SELECT 
    DATE(HR.Created_At) AS RequestDate,
    COUNT(HR.Request_ID) AS RequestCount
FROM 
    Health_Request HR
INNER JOIN 
	HealthRequest_Status_Relation HRS on HRS.Request_ID = HR.Request_ID
INNER JOIN 
    RequestStatus RS ON HRS.StatusID = RS.StatusID
INNER JOIN 
    HealthRequest_Student_Course_Relation RSR ON HR.Request_ID = RSR.Request_ID
INNER JOIN 
    Student DS ON RSR.StudentID = DS.StudentID
WHERE 
    Date(HR.Created_At) = '{dateString}'
GROUP BY 
    DATE(HR.Created_At);
    """)
    return db_cursor.fetchall()

def getRequestFromStudent(db_cursor, firstName, lastName):
    db_cursor.execute(f"""
SELECT 
	concat(s.FirstName, ' ', s.LastName) as Name,
    hr.Request_ID, 
    hr.Symptoms AS Request_Detail, 
    hr.Created_At AS Request_Date 
FROM 
    Student s
INNER JOIN 
    HealthRequest_Student_Course_Relation rsr ON s.StudentID = rsr.StudentID
INNER JOIN 
    Health_Request hr ON rsr.Request_ID = hr.Request_ID
WHERE 
    s.FirstName LIKE '{firstName}' AND s.LastName LIKE '{lastName}'
ORDER BY 
    hr.Created_At ASC;

    """)
    return db_cursor.fetchall()

def getStudentsNoRequests(db_cursor):
    db_cursor.execute("""
    SELECT s.StudentID, s.FirstName, s.LastName, s.Email
    FROM Student s
    LEFT JOIN HealthRequest_Student_Course_Relation rsr ON s.StudentID = rsr.StudentID
    WHERE rsr.Request_ID IS NULL
    ORDER BY s.StudentID;
                      """)
    return db_cursor.fetchall()

def getHealthRequestAndStudentForEachStatus(db_cursor):
    db_cursor.execute("""
    SELECT 
    StatusName, 
    s.FirstName, 
    s.LastName, 
    s.StudentID,
    COUNT(*) AS request_count
FROM 
    Health_Request HR
INNER JOIN
	HealthRequest_Status_Relation HSR ON HSR.Request_ID = HR.Request_ID
INNER JOIN 
	RequestStatus RS ON RS.StatusID = HSR.StatusID
INNER JOIN 
    HealthRequest_Student_Course_Relation RSR ON HR.Request_ID = RSR.Request_ID
INNER JOIN 
    Student s ON RSR.StudentID = s.StudentID
GROUP BY 
    StatusName, s.FirstName, s.LastName, s.StudentID
ORDER BY 
    StatusName, s.LastName, s.FirstName;
    """)
    return db_cursor.fetchall()

def getAllRequests(db_cursor):
    db_cursor.execute("""
    select * from Health_Request
    """)
    return db_cursor.fetchall()

def getAllStudents(db_cursor):
    db_cursor.execute("select * from Student")
    return db_cursor.fetchall()

def getAllHealthPersonnel(db_cursor):
    db_cursor.execute("select * from Health_Personnel")
    return db_cursor.fetchall()

def getApprovedBy(db_cursor):
    db_cursor.execute('select * from Approved_By')
    return db_cursor.fetchall()

    