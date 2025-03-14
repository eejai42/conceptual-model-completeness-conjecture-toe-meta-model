
    SET ANSI_NULLS ON
    GO

    SET QUOTED_IDENTIFIER ON
    GO
    
    
      -- TABLE: JsonWrapper
      -- TABLE: Meta-model
      -- TABLE: Meta
      -- TABLE: Executive_summary
      -- TABLE: Narrative
      -- TABLE: Addressing_concerns_preemptively
      -- TABLE: Schema
      -- TABLE: Entity
      -- TABLE: Field
      -- TABLE: Lookup
      -- TABLE: Aggregation
      -- TABLE: Lambda
      -- TABLE: Constraint
      -- TABLE: Datum
      -- TABLE: Conference
      -- TABLE: ConferenceDay
      -- TABLE: Room
      -- TABLE: Session
      -- TABLE: Speaker
      -- TABLE: Attendee
      -- TABLE: SessionAttendanceEvent
      -- TABLE: Sponsor
      -- TABLE: ConferencePolicy
      -- TABLE: SampleExtraSession
      -- TABLE: SampleSpeakerAssignment
      -- TABLE: SampleAttendanceAction
      -- TABLE: Root-meta-model
      -- TABLE: Author
      -- TABLE: Section
      -- TABLE: CMCC_ToEMM_Domain_List

      -- CREATE DATABASE
      IF NOT EXISTS (SELECT * from sys.databases WHERE name = 'OntologySchema')
      BEGIN
          CREATE DATABASE [OntologySchema];
      END
        GO
        
     USE [OntologySchema];
GO
      
        -- TABLE: JsonWrapper -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[JsonWrapper]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[JsonWrapper]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[JsonWrapper] (
          [JsonWrapperId] INT NOT NULL
          -- int.
        ,
          [Id] NVARCHAR(100) NOT NULL
          -- string.
        ,
        
        CONSTRAINT [PK_JsonWrapper] PRIMARY KEY CLUSTERED
          (
            [JsonWrapperId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Meta-model -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Meta-model]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Meta-model]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Meta-model] (
          [Meta-modelId] INT NOT NULL
          -- int.
        ,
          [Name] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Description] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Version] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Nickname] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [JsonWrapperId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Meta-model] PRIMARY KEY CLUSTERED
          (
            [Meta-modelId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Meta -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Meta]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Meta]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Meta] (
          [MetaId] INT NOT NULL
          -- int.
        ,
          [Title] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Subtitle] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Date] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Abstract] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Meta-modelId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Meta] PRIMARY KEY CLUSTERED
          (
            [MetaId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Executive_summary -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Executive_summary]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Executive_summary]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Executive_summary] (
          [Executive_summaryId] INT NOT NULL
          -- int.
        ,
          [Key_points] NVARCHAR(100) NOT NULL
          -- String.
        ,
          [Implications] NVARCHAR(100) NOT NULL
          -- String.
        ,
          [MetaId] INT NOT NULL
          -- int.
        ,
          [Root-meta-modelId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Executive_summary] PRIMARY KEY CLUSTERED
          (
            [Executive_summaryId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Narrative -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Narrative]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Narrative]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Narrative] (
          [NarrativeId] INT NOT NULL
          -- int.
        ,
          [Title] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Content] NVARCHAR(100) NOT NULL
          -- String.
        ,
          [Executive_summaryId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Narrative] PRIMARY KEY CLUSTERED
          (
            [NarrativeId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Addressing_concerns_preemptively -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Addressing_concerns_preemptively]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Addressing_concerns_preemptively]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Addressing_concerns_preemptively] (
          [Addressing_concerns_preemptivelyId] INT NOT NULL
          -- int.
        ,
          [What_not_how] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Time] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Rulebook_not_the_runtime] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Scaleability_performance] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Reality_is_the_best_runtime_engine] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Bright_red_lines] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Executive_summaryId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Addressing_concerns_preemptively] PRIMARY KEY CLUSTERED
          (
            [Addressing_concerns_preemptivelyId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Schema -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Schema]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Schema]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Schema] (
          [SchemaId] INT NOT NULL
          -- int.
        ,
          [Meta-modelId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Schema] PRIMARY KEY CLUSTERED
          (
            [SchemaId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Entity -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Entity]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Entity]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Entity] (
          [EntityId] INT NOT NULL
          -- int.
        ,
          [Name] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Description] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Lookups] NVARCHAR(100) NOT NULL
          -- String.
        ,
          [Aggregations] NVARCHAR(100) NOT NULL
          -- String.
        ,
          [Lambdas] NVARCHAR(100) NOT NULL
          -- String.
        ,
          [Constraints] NVARCHAR(100) NOT NULL
          -- String.
        ,
          [SchemaId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Entity] PRIMARY KEY CLUSTERED
          (
            [EntityId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Field -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Field]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Field]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Field] (
          [FieldId] INT NOT NULL
          -- int.
        ,
          [Name] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Type] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Datatype] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Primary_key] BIT NOT NULL
          -- bool.
        ,
          [Description] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [EntityId] INT NOT NULL
          -- int.
        ,
          [Target_entity] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Foreign_key] BIT NOT NULL
          -- bool.
        ,
        
        CONSTRAINT [PK_Field] PRIMARY KEY CLUSTERED
          (
            [FieldId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Lookup -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Lookup]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Lookup]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Lookup] (
          [LookupId] INT NOT NULL
          -- int.
        ,
          [Name] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Target_entity] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Type] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Join_condition] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Description] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [EntityId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Lookup] PRIMARY KEY CLUSTERED
          (
            [LookupId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Aggregation -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Aggregation]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Aggregation]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Aggregation] (
          [AggregationId] INT NOT NULL
          -- int.
        ,
          [Name] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Type] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Description] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Formula] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [EntityId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Aggregation] PRIMARY KEY CLUSTERED
          (
            [AggregationId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Lambda -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Lambda]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Lambda]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Lambda] (
          [LambdaId] INT NOT NULL
          -- int.
        ,
          [Name] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Parameters] NVARCHAR(100) NOT NULL
          -- String.
        ,
          [Description] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Formula] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [EntityId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Lambda] PRIMARY KEY CLUSTERED
          (
            [LambdaId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Constraint -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Constraint]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Constraint]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Constraint] (
          [ConstraintId] INT NOT NULL
          -- int.
        ,
          [Name] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Formula] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Error_message] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [EntityId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Constraint] PRIMARY KEY CLUSTERED
          (
            [ConstraintId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Datum -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Datum]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Datum]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Datum] (
          [DatumId] INT NOT NULL
          -- int.
        ,
          [SessionEndEvent] NVARCHAR(100) NOT NULL
          -- String.
        ,
          [AttendeeDayCheckInEvent] NVARCHAR(100) NOT NULL
          -- String.
        ,
          [SchemaId] INT NOT NULL
          -- int.
        ,
          [Meta-modelId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Datum] PRIMARY KEY CLUSTERED
          (
            [DatumId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Conference -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Conference]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Conference]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Conference] (
          [ConferenceId] INT NOT NULL
          -- int.
        ,
          [Id] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [ConferenceName] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Location] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [DatumId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Conference] PRIMARY KEY CLUSTERED
          (
            [ConferenceId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: ConferenceDay -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[ConferenceDay]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ConferenceDay]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[ConferenceDay] (
          [ConferenceDayId] INT NOT NULL
          -- int.
        ,
          [Id] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [ConferenceId] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [DayDate] DATETIME NOT NULL
          -- datetime.
        ,
          [StartTime] DATETIME NOT NULL
          -- datetime.
        ,
          [EndTime] DATETIME NOT NULL
          -- datetime.
        ,
          [DatumId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_ConferenceDay] PRIMARY KEY CLUSTERED
          (
            [ConferenceDayId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Room -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Room]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Room]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Room] (
          [RoomId] INT NOT NULL
          -- int.
        ,
          [Id] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [ConferenceId] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [RoomName] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Capacity] INT NOT NULL
          -- int.
        ,
          [DatumId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Room] PRIMARY KEY CLUSTERED
          (
            [RoomId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Session -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Session]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Session]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Session] (
          [SessionId] INT NOT NULL
          -- int.
        ,
          [Id] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [DayId] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [RoomId] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [SessionTitle] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [StartTime] DATETIME NOT NULL
          -- datetime.
        ,
          [EndTime] DATETIME NOT NULL
          -- datetime.
        ,
          [SessionType] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [IsCanceled] BIT NOT NULL
          -- bool.
        ,
          [DatumId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Session] PRIMARY KEY CLUSTERED
          (
            [SessionId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Speaker -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Speaker]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Speaker]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Speaker] (
          [SpeakerId] INT NOT NULL
          -- int.
        ,
          [Id] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [ConferenceId] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [FullName] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Bio] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [DatumId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Speaker] PRIMARY KEY CLUSTERED
          (
            [SpeakerId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Attendee -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Attendee]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Attendee]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Attendee] (
          [AttendeeId] INT NOT NULL
          -- int.
        ,
          [Id] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [FullName] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [DatumId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Attendee] PRIMARY KEY CLUSTERED
          (
            [AttendeeId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: SessionAttendanceEvent -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[SessionAttendanceEvent]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[SessionAttendanceEvent]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[SessionAttendanceEvent] (
          [SessionAttendanceEventId] INT NOT NULL
          -- int.
        ,
          [Id] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [SessionId] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [AttendeeId] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [CheckInTime] DATETIME NOT NULL
          -- datetime.
        ,
          [CheckOutTime] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [DatumId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_SessionAttendanceEvent] PRIMARY KEY CLUSTERED
          (
            [SessionAttendanceEventId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Sponsor -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Sponsor]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Sponsor]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Sponsor] (
          [SponsorId] INT NOT NULL
          -- int.
        ,
          [Id] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [ConferenceId] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [SponsorName] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [SponsorTier] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [DatumId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Sponsor] PRIMARY KEY CLUSTERED
          (
            [SponsorId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: ConferencePolicy -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[ConferencePolicy]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ConferencePolicy]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[ConferencePolicy] (
          [ConferencePolicyId] INT NOT NULL
          -- int.
        ,
          [Id] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [ConferenceId] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [MaxSessionLengthMinutes] INT NOT NULL
          -- int.
        ,
          [MinBreakBetweenSessionsMinutes] INT NOT NULL
          -- int.
        ,
          [RoomChangeBufferMinutes] INT NOT NULL
          -- int.
        ,
          [DatumId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_ConferencePolicy] PRIMARY KEY CLUSTERED
          (
            [ConferencePolicyId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: SampleExtraSession -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[SampleExtraSession]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[SampleExtraSession]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[SampleExtraSession] (
          [SampleExtraSessionId] INT NOT NULL
          -- int.
        ,
          [Id] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [DayId] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [RoomId] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [SessionTitle] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [StartTime] DATETIME NOT NULL
          -- datetime.
        ,
          [EndTime] DATETIME NOT NULL
          -- datetime.
        ,
          [SessionType] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [IsCanceled] BIT NOT NULL
          -- bool.
        ,
          [DatumId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_SampleExtraSession] PRIMARY KEY CLUSTERED
          (
            [SampleExtraSessionId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: SampleSpeakerAssignment -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[SampleSpeakerAssignment]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[SampleSpeakerAssignment]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[SampleSpeakerAssignment] (
          [SampleSpeakerAssignmentId] INT NOT NULL
          -- int.
        ,
          [SpeakerId] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [SessionId] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [DatumId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_SampleSpeakerAssignment] PRIMARY KEY CLUSTERED
          (
            [SampleSpeakerAssignmentId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: SampleAttendanceAction -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[SampleAttendanceAction]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[SampleAttendanceAction]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[SampleAttendanceAction] (
          [SampleAttendanceActionId] INT NOT NULL
          -- int.
        ,
          [Id] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [SessionId] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [AttendeeId] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [CheckInTime] DATETIME NOT NULL
          -- datetime.
        ,
          [DatumId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_SampleAttendanceAction] PRIMARY KEY CLUSTERED
          (
            [SampleAttendanceActionId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Root-meta-model -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Root-meta-model]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Root-meta-model]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Root-meta-model] (
          [Root-meta-modelId] INT NOT NULL
          -- int.
        ,
          [Title] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Subtitle] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Date] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Abstract] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Meta-modelId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Root-meta-model] PRIMARY KEY CLUSTERED
          (
            [Root-meta-modelId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Author -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Author]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Author]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Author] (
          [AuthorId] INT NOT NULL
          -- int.
        ,
          [Name] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Contact] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Affiliations] NVARCHAR(100) NOT NULL
          -- String.
        ,
          [Root-meta-modelId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Author] PRIMARY KEY CLUSTERED
          (
            [AuthorId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: Section -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[Section]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Section]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[Section] (
          [SectionId] INT NOT NULL
          -- int.
        ,
          [Title] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Content] NVARCHAR(100) NOT NULL
          -- String.
        ,
          [NarrativeId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_Section] PRIMARY KEY CLUSTERED
          (
            [SectionId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO

        -- TABLE: CMCC_ToEMM_Domain_List -- EXCLUDE READONLY: false
        -- ****** Object:  Table [dbo].[CMCC_ToEMM_Domain_List]   Script Date:  ******
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[CMCC_ToEMM_Domain_List]') AND type in (N'U')) 
        BEGIN
        CREATE TABLE [dbo].[CMCC_ToEMM_Domain_List] (
          [CMCC_ToEMM_Domain_ListId] INT NOT NULL
          -- int.
        ,
          [Id] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Fullname] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Name] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Description] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Nickname] NVARCHAR(100) NOT NULL
          -- string.
        ,
          [Root-meta-modelId] INT NOT NULL
          -- int.
        ,
        
        CONSTRAINT [PK_CMCC_ToEMM_Domain_List] PRIMARY KEY CLUSTERED
          (
            [CMCC_ToEMM_Domain_ListId] ASC
          )
        
        ) ON [PRIMARY]
        END
        GO


      
DECLARE @ObjectName NVARCHAR(100)

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'JsonWrapperId' AND Object_ID = Object_ID(N'JsonWrapper'))
    BEGIN
            ALTER TABLE [dbo].[JsonWrapper] ADD [JsonWrapperId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Id' AND Object_ID = Object_ID(N'JsonWrapper'))
    BEGIN
            ALTER TABLE [dbo].[JsonWrapper] ADD [Id] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Meta-modelId' AND Object_ID = Object_ID(N'Meta-model'))
    BEGIN
            ALTER TABLE [dbo].[Meta-model] ADD [Meta-modelId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Name' AND Object_ID = Object_ID(N'Meta-model'))
    BEGIN
            ALTER TABLE [dbo].[Meta-model] ADD [Name] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Description' AND Object_ID = Object_ID(N'Meta-model'))
    BEGIN
            ALTER TABLE [dbo].[Meta-model] ADD [Description] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Version' AND Object_ID = Object_ID(N'Meta-model'))
    BEGIN
            ALTER TABLE [dbo].[Meta-model] ADD [Version] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Nickname' AND Object_ID = Object_ID(N'Meta-model'))
    BEGIN
            ALTER TABLE [dbo].[Meta-model] ADD [Nickname] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'JsonWrapperId' AND Object_ID = Object_ID(N'Meta-model'))
    BEGIN
            ALTER TABLE [dbo].[Meta-model] ADD [JsonWrapperId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'MetaId' AND Object_ID = Object_ID(N'Meta'))
    BEGIN
            ALTER TABLE [dbo].[Meta] ADD [MetaId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Title' AND Object_ID = Object_ID(N'Meta'))
    BEGIN
            ALTER TABLE [dbo].[Meta] ADD [Title] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Subtitle' AND Object_ID = Object_ID(N'Meta'))
    BEGIN
            ALTER TABLE [dbo].[Meta] ADD [Subtitle] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Date' AND Object_ID = Object_ID(N'Meta'))
    BEGIN
            ALTER TABLE [dbo].[Meta] ADD [Date] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Abstract' AND Object_ID = Object_ID(N'Meta'))
    BEGIN
            ALTER TABLE [dbo].[Meta] ADD [Abstract] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Meta-modelId' AND Object_ID = Object_ID(N'Meta'))
    BEGIN
            ALTER TABLE [dbo].[Meta] ADD [Meta-modelId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Executive_summaryId' AND Object_ID = Object_ID(N'Executive_summary'))
    BEGIN
            ALTER TABLE [dbo].[Executive_summary] ADD [Executive_summaryId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Key_points' AND Object_ID = Object_ID(N'Executive_summary'))
    BEGIN
            ALTER TABLE [dbo].[Executive_summary] ADD [Key_points] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Implications' AND Object_ID = Object_ID(N'Executive_summary'))
    BEGIN
            ALTER TABLE [dbo].[Executive_summary] ADD [Implications] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'MetaId' AND Object_ID = Object_ID(N'Executive_summary'))
    BEGIN
            ALTER TABLE [dbo].[Executive_summary] ADD [MetaId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Root-meta-modelId' AND Object_ID = Object_ID(N'Executive_summary'))
    BEGIN
            ALTER TABLE [dbo].[Executive_summary] ADD [Root-meta-modelId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'NarrativeId' AND Object_ID = Object_ID(N'Narrative'))
    BEGIN
            ALTER TABLE [dbo].[Narrative] ADD [NarrativeId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Title' AND Object_ID = Object_ID(N'Narrative'))
    BEGIN
            ALTER TABLE [dbo].[Narrative] ADD [Title] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Content' AND Object_ID = Object_ID(N'Narrative'))
    BEGIN
            ALTER TABLE [dbo].[Narrative] ADD [Content] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Executive_summaryId' AND Object_ID = Object_ID(N'Narrative'))
    BEGIN
            ALTER TABLE [dbo].[Narrative] ADD [Executive_summaryId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Addressing_concerns_preemptivelyId' AND Object_ID = Object_ID(N'Addressing_concerns_preemptively'))
    BEGIN
            ALTER TABLE [dbo].[Addressing_concerns_preemptively] ADD [Addressing_concerns_preemptivelyId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'What_not_how' AND Object_ID = Object_ID(N'Addressing_concerns_preemptively'))
    BEGIN
            ALTER TABLE [dbo].[Addressing_concerns_preemptively] ADD [What_not_how] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Time' AND Object_ID = Object_ID(N'Addressing_concerns_preemptively'))
    BEGIN
            ALTER TABLE [dbo].[Addressing_concerns_preemptively] ADD [Time] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Rulebook_not_the_runtime' AND Object_ID = Object_ID(N'Addressing_concerns_preemptively'))
    BEGIN
            ALTER TABLE [dbo].[Addressing_concerns_preemptively] ADD [Rulebook_not_the_runtime] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Scaleability_performance' AND Object_ID = Object_ID(N'Addressing_concerns_preemptively'))
    BEGIN
            ALTER TABLE [dbo].[Addressing_concerns_preemptively] ADD [Scaleability_performance] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Reality_is_the_best_runtime_engine' AND Object_ID = Object_ID(N'Addressing_concerns_preemptively'))
    BEGIN
            ALTER TABLE [dbo].[Addressing_concerns_preemptively] ADD [Reality_is_the_best_runtime_engine] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Bright_red_lines' AND Object_ID = Object_ID(N'Addressing_concerns_preemptively'))
    BEGIN
            ALTER TABLE [dbo].[Addressing_concerns_preemptively] ADD [Bright_red_lines] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Executive_summaryId' AND Object_ID = Object_ID(N'Addressing_concerns_preemptively'))
    BEGIN
            ALTER TABLE [dbo].[Addressing_concerns_preemptively] ADD [Executive_summaryId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SchemaId' AND Object_ID = Object_ID(N'Schema'))
    BEGIN
            ALTER TABLE [dbo].[Schema] ADD [SchemaId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Meta-modelId' AND Object_ID = Object_ID(N'Schema'))
    BEGIN
            ALTER TABLE [dbo].[Schema] ADD [Meta-modelId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'EntityId' AND Object_ID = Object_ID(N'Entity'))
    BEGIN
            ALTER TABLE [dbo].[Entity] ADD [EntityId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Name' AND Object_ID = Object_ID(N'Entity'))
    BEGIN
            ALTER TABLE [dbo].[Entity] ADD [Name] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Description' AND Object_ID = Object_ID(N'Entity'))
    BEGIN
            ALTER TABLE [dbo].[Entity] ADD [Description] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Lookups' AND Object_ID = Object_ID(N'Entity'))
    BEGIN
            ALTER TABLE [dbo].[Entity] ADD [Lookups] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Aggregations' AND Object_ID = Object_ID(N'Entity'))
    BEGIN
            ALTER TABLE [dbo].[Entity] ADD [Aggregations] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Lambdas' AND Object_ID = Object_ID(N'Entity'))
    BEGIN
            ALTER TABLE [dbo].[Entity] ADD [Lambdas] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Constraints' AND Object_ID = Object_ID(N'Entity'))
    BEGIN
            ALTER TABLE [dbo].[Entity] ADD [Constraints] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SchemaId' AND Object_ID = Object_ID(N'Entity'))
    BEGIN
            ALTER TABLE [dbo].[Entity] ADD [SchemaId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'FieldId' AND Object_ID = Object_ID(N'Field'))
    BEGIN
            ALTER TABLE [dbo].[Field] ADD [FieldId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Name' AND Object_ID = Object_ID(N'Field'))
    BEGIN
            ALTER TABLE [dbo].[Field] ADD [Name] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Type' AND Object_ID = Object_ID(N'Field'))
    BEGIN
            ALTER TABLE [dbo].[Field] ADD [Type] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Datatype' AND Object_ID = Object_ID(N'Field'))
    BEGIN
            ALTER TABLE [dbo].[Field] ADD [Datatype] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Primary_key' AND Object_ID = Object_ID(N'Field'))
    BEGIN
            ALTER TABLE [dbo].[Field] ADD [Primary_key] BIT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Description' AND Object_ID = Object_ID(N'Field'))
    BEGIN
            ALTER TABLE [dbo].[Field] ADD [Description] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'EntityId' AND Object_ID = Object_ID(N'Field'))
    BEGIN
            ALTER TABLE [dbo].[Field] ADD [EntityId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Target_entity' AND Object_ID = Object_ID(N'Field'))
    BEGIN
            ALTER TABLE [dbo].[Field] ADD [Target_entity] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Foreign_key' AND Object_ID = Object_ID(N'Field'))
    BEGIN
            ALTER TABLE [dbo].[Field] ADD [Foreign_key] BIT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'LookupId' AND Object_ID = Object_ID(N'Lookup'))
    BEGIN
            ALTER TABLE [dbo].[Lookup] ADD [LookupId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Name' AND Object_ID = Object_ID(N'Lookup'))
    BEGIN
            ALTER TABLE [dbo].[Lookup] ADD [Name] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Target_entity' AND Object_ID = Object_ID(N'Lookup'))
    BEGIN
            ALTER TABLE [dbo].[Lookup] ADD [Target_entity] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Type' AND Object_ID = Object_ID(N'Lookup'))
    BEGIN
            ALTER TABLE [dbo].[Lookup] ADD [Type] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Join_condition' AND Object_ID = Object_ID(N'Lookup'))
    BEGIN
            ALTER TABLE [dbo].[Lookup] ADD [Join_condition] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Description' AND Object_ID = Object_ID(N'Lookup'))
    BEGIN
            ALTER TABLE [dbo].[Lookup] ADD [Description] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'EntityId' AND Object_ID = Object_ID(N'Lookup'))
    BEGIN
            ALTER TABLE [dbo].[Lookup] ADD [EntityId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'AggregationId' AND Object_ID = Object_ID(N'Aggregation'))
    BEGIN
            ALTER TABLE [dbo].[Aggregation] ADD [AggregationId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Name' AND Object_ID = Object_ID(N'Aggregation'))
    BEGIN
            ALTER TABLE [dbo].[Aggregation] ADD [Name] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Type' AND Object_ID = Object_ID(N'Aggregation'))
    BEGIN
            ALTER TABLE [dbo].[Aggregation] ADD [Type] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Description' AND Object_ID = Object_ID(N'Aggregation'))
    BEGIN
            ALTER TABLE [dbo].[Aggregation] ADD [Description] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Formula' AND Object_ID = Object_ID(N'Aggregation'))
    BEGIN
            ALTER TABLE [dbo].[Aggregation] ADD [Formula] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'EntityId' AND Object_ID = Object_ID(N'Aggregation'))
    BEGIN
            ALTER TABLE [dbo].[Aggregation] ADD [EntityId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'LambdaId' AND Object_ID = Object_ID(N'Lambda'))
    BEGIN
            ALTER TABLE [dbo].[Lambda] ADD [LambdaId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Name' AND Object_ID = Object_ID(N'Lambda'))
    BEGIN
            ALTER TABLE [dbo].[Lambda] ADD [Name] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Parameters' AND Object_ID = Object_ID(N'Lambda'))
    BEGIN
            ALTER TABLE [dbo].[Lambda] ADD [Parameters] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Description' AND Object_ID = Object_ID(N'Lambda'))
    BEGIN
            ALTER TABLE [dbo].[Lambda] ADD [Description] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Formula' AND Object_ID = Object_ID(N'Lambda'))
    BEGIN
            ALTER TABLE [dbo].[Lambda] ADD [Formula] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'EntityId' AND Object_ID = Object_ID(N'Lambda'))
    BEGIN
            ALTER TABLE [dbo].[Lambda] ADD [EntityId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'ConstraintId' AND Object_ID = Object_ID(N'Constraint'))
    BEGIN
            ALTER TABLE [dbo].[Constraint] ADD [ConstraintId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Name' AND Object_ID = Object_ID(N'Constraint'))
    BEGIN
            ALTER TABLE [dbo].[Constraint] ADD [Name] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Formula' AND Object_ID = Object_ID(N'Constraint'))
    BEGIN
            ALTER TABLE [dbo].[Constraint] ADD [Formula] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Error_message' AND Object_ID = Object_ID(N'Constraint'))
    BEGIN
            ALTER TABLE [dbo].[Constraint] ADD [Error_message] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'EntityId' AND Object_ID = Object_ID(N'Constraint'))
    BEGIN
            ALTER TABLE [dbo].[Constraint] ADD [EntityId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'DatumId' AND Object_ID = Object_ID(N'Datum'))
    BEGIN
            ALTER TABLE [dbo].[Datum] ADD [DatumId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SessionEndEvent' AND Object_ID = Object_ID(N'Datum'))
    BEGIN
            ALTER TABLE [dbo].[Datum] ADD [SessionEndEvent] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'AttendeeDayCheckInEvent' AND Object_ID = Object_ID(N'Datum'))
    BEGIN
            ALTER TABLE [dbo].[Datum] ADD [AttendeeDayCheckInEvent] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SchemaId' AND Object_ID = Object_ID(N'Datum'))
    BEGIN
            ALTER TABLE [dbo].[Datum] ADD [SchemaId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Meta-modelId' AND Object_ID = Object_ID(N'Datum'))
    BEGIN
            ALTER TABLE [dbo].[Datum] ADD [Meta-modelId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'ConferenceId' AND Object_ID = Object_ID(N'Conference'))
    BEGIN
            ALTER TABLE [dbo].[Conference] ADD [ConferenceId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Id' AND Object_ID = Object_ID(N'Conference'))
    BEGIN
            ALTER TABLE [dbo].[Conference] ADD [Id] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'ConferenceName' AND Object_ID = Object_ID(N'Conference'))
    BEGIN
            ALTER TABLE [dbo].[Conference] ADD [ConferenceName] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Location' AND Object_ID = Object_ID(N'Conference'))
    BEGIN
            ALTER TABLE [dbo].[Conference] ADD [Location] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'DatumId' AND Object_ID = Object_ID(N'Conference'))
    BEGIN
            ALTER TABLE [dbo].[Conference] ADD [DatumId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'ConferenceDayId' AND Object_ID = Object_ID(N'ConferenceDay'))
    BEGIN
            ALTER TABLE [dbo].[ConferenceDay] ADD [ConferenceDayId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Id' AND Object_ID = Object_ID(N'ConferenceDay'))
    BEGIN
            ALTER TABLE [dbo].[ConferenceDay] ADD [Id] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'ConferenceId' AND Object_ID = Object_ID(N'ConferenceDay'))
    BEGIN
            ALTER TABLE [dbo].[ConferenceDay] ADD [ConferenceId] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'DayDate' AND Object_ID = Object_ID(N'ConferenceDay'))
    BEGIN
            ALTER TABLE [dbo].[ConferenceDay] ADD [DayDate] DATETIME NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'StartTime' AND Object_ID = Object_ID(N'ConferenceDay'))
    BEGIN
            ALTER TABLE [dbo].[ConferenceDay] ADD [StartTime] DATETIME NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'EndTime' AND Object_ID = Object_ID(N'ConferenceDay'))
    BEGIN
            ALTER TABLE [dbo].[ConferenceDay] ADD [EndTime] DATETIME NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'DatumId' AND Object_ID = Object_ID(N'ConferenceDay'))
    BEGIN
            ALTER TABLE [dbo].[ConferenceDay] ADD [DatumId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'RoomId' AND Object_ID = Object_ID(N'Room'))
    BEGIN
            ALTER TABLE [dbo].[Room] ADD [RoomId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Id' AND Object_ID = Object_ID(N'Room'))
    BEGIN
            ALTER TABLE [dbo].[Room] ADD [Id] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'ConferenceId' AND Object_ID = Object_ID(N'Room'))
    BEGIN
            ALTER TABLE [dbo].[Room] ADD [ConferenceId] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'RoomName' AND Object_ID = Object_ID(N'Room'))
    BEGIN
            ALTER TABLE [dbo].[Room] ADD [RoomName] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Capacity' AND Object_ID = Object_ID(N'Room'))
    BEGIN
            ALTER TABLE [dbo].[Room] ADD [Capacity] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'DatumId' AND Object_ID = Object_ID(N'Room'))
    BEGIN
            ALTER TABLE [dbo].[Room] ADD [DatumId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SessionId' AND Object_ID = Object_ID(N'Session'))
    BEGIN
            ALTER TABLE [dbo].[Session] ADD [SessionId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Id' AND Object_ID = Object_ID(N'Session'))
    BEGIN
            ALTER TABLE [dbo].[Session] ADD [Id] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'DayId' AND Object_ID = Object_ID(N'Session'))
    BEGIN
            ALTER TABLE [dbo].[Session] ADD [DayId] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'RoomId' AND Object_ID = Object_ID(N'Session'))
    BEGIN
            ALTER TABLE [dbo].[Session] ADD [RoomId] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SessionTitle' AND Object_ID = Object_ID(N'Session'))
    BEGIN
            ALTER TABLE [dbo].[Session] ADD [SessionTitle] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'StartTime' AND Object_ID = Object_ID(N'Session'))
    BEGIN
            ALTER TABLE [dbo].[Session] ADD [StartTime] DATETIME NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'EndTime' AND Object_ID = Object_ID(N'Session'))
    BEGIN
            ALTER TABLE [dbo].[Session] ADD [EndTime] DATETIME NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SessionType' AND Object_ID = Object_ID(N'Session'))
    BEGIN
            ALTER TABLE [dbo].[Session] ADD [SessionType] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'IsCanceled' AND Object_ID = Object_ID(N'Session'))
    BEGIN
            ALTER TABLE [dbo].[Session] ADD [IsCanceled] BIT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'DatumId' AND Object_ID = Object_ID(N'Session'))
    BEGIN
            ALTER TABLE [dbo].[Session] ADD [DatumId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SpeakerId' AND Object_ID = Object_ID(N'Speaker'))
    BEGIN
            ALTER TABLE [dbo].[Speaker] ADD [SpeakerId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Id' AND Object_ID = Object_ID(N'Speaker'))
    BEGIN
            ALTER TABLE [dbo].[Speaker] ADD [Id] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'ConferenceId' AND Object_ID = Object_ID(N'Speaker'))
    BEGIN
            ALTER TABLE [dbo].[Speaker] ADD [ConferenceId] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'FullName' AND Object_ID = Object_ID(N'Speaker'))
    BEGIN
            ALTER TABLE [dbo].[Speaker] ADD [FullName] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Bio' AND Object_ID = Object_ID(N'Speaker'))
    BEGIN
            ALTER TABLE [dbo].[Speaker] ADD [Bio] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'DatumId' AND Object_ID = Object_ID(N'Speaker'))
    BEGIN
            ALTER TABLE [dbo].[Speaker] ADD [DatumId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'AttendeeId' AND Object_ID = Object_ID(N'Attendee'))
    BEGIN
            ALTER TABLE [dbo].[Attendee] ADD [AttendeeId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Id' AND Object_ID = Object_ID(N'Attendee'))
    BEGIN
            ALTER TABLE [dbo].[Attendee] ADD [Id] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'FullName' AND Object_ID = Object_ID(N'Attendee'))
    BEGIN
            ALTER TABLE [dbo].[Attendee] ADD [FullName] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'DatumId' AND Object_ID = Object_ID(N'Attendee'))
    BEGIN
            ALTER TABLE [dbo].[Attendee] ADD [DatumId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SessionAttendanceEventId' AND Object_ID = Object_ID(N'SessionAttendanceEvent'))
    BEGIN
            ALTER TABLE [dbo].[SessionAttendanceEvent] ADD [SessionAttendanceEventId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Id' AND Object_ID = Object_ID(N'SessionAttendanceEvent'))
    BEGIN
            ALTER TABLE [dbo].[SessionAttendanceEvent] ADD [Id] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SessionId' AND Object_ID = Object_ID(N'SessionAttendanceEvent'))
    BEGIN
            ALTER TABLE [dbo].[SessionAttendanceEvent] ADD [SessionId] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'AttendeeId' AND Object_ID = Object_ID(N'SessionAttendanceEvent'))
    BEGIN
            ALTER TABLE [dbo].[SessionAttendanceEvent] ADD [AttendeeId] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'CheckInTime' AND Object_ID = Object_ID(N'SessionAttendanceEvent'))
    BEGIN
            ALTER TABLE [dbo].[SessionAttendanceEvent] ADD [CheckInTime] DATETIME NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'CheckOutTime' AND Object_ID = Object_ID(N'SessionAttendanceEvent'))
    BEGIN
            ALTER TABLE [dbo].[SessionAttendanceEvent] ADD [CheckOutTime] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'DatumId' AND Object_ID = Object_ID(N'SessionAttendanceEvent'))
    BEGIN
            ALTER TABLE [dbo].[SessionAttendanceEvent] ADD [DatumId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SponsorId' AND Object_ID = Object_ID(N'Sponsor'))
    BEGIN
            ALTER TABLE [dbo].[Sponsor] ADD [SponsorId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Id' AND Object_ID = Object_ID(N'Sponsor'))
    BEGIN
            ALTER TABLE [dbo].[Sponsor] ADD [Id] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'ConferenceId' AND Object_ID = Object_ID(N'Sponsor'))
    BEGIN
            ALTER TABLE [dbo].[Sponsor] ADD [ConferenceId] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SponsorName' AND Object_ID = Object_ID(N'Sponsor'))
    BEGIN
            ALTER TABLE [dbo].[Sponsor] ADD [SponsorName] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SponsorTier' AND Object_ID = Object_ID(N'Sponsor'))
    BEGIN
            ALTER TABLE [dbo].[Sponsor] ADD [SponsorTier] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'DatumId' AND Object_ID = Object_ID(N'Sponsor'))
    BEGIN
            ALTER TABLE [dbo].[Sponsor] ADD [DatumId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'ConferencePolicyId' AND Object_ID = Object_ID(N'ConferencePolicy'))
    BEGIN
            ALTER TABLE [dbo].[ConferencePolicy] ADD [ConferencePolicyId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Id' AND Object_ID = Object_ID(N'ConferencePolicy'))
    BEGIN
            ALTER TABLE [dbo].[ConferencePolicy] ADD [Id] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'ConferenceId' AND Object_ID = Object_ID(N'ConferencePolicy'))
    BEGIN
            ALTER TABLE [dbo].[ConferencePolicy] ADD [ConferenceId] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'MaxSessionLengthMinutes' AND Object_ID = Object_ID(N'ConferencePolicy'))
    BEGIN
            ALTER TABLE [dbo].[ConferencePolicy] ADD [MaxSessionLengthMinutes] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'MinBreakBetweenSessionsMinutes' AND Object_ID = Object_ID(N'ConferencePolicy'))
    BEGIN
            ALTER TABLE [dbo].[ConferencePolicy] ADD [MinBreakBetweenSessionsMinutes] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'RoomChangeBufferMinutes' AND Object_ID = Object_ID(N'ConferencePolicy'))
    BEGIN
            ALTER TABLE [dbo].[ConferencePolicy] ADD [RoomChangeBufferMinutes] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'DatumId' AND Object_ID = Object_ID(N'ConferencePolicy'))
    BEGIN
            ALTER TABLE [dbo].[ConferencePolicy] ADD [DatumId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SampleExtraSessionId' AND Object_ID = Object_ID(N'SampleExtraSession'))
    BEGIN
            ALTER TABLE [dbo].[SampleExtraSession] ADD [SampleExtraSessionId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Id' AND Object_ID = Object_ID(N'SampleExtraSession'))
    BEGIN
            ALTER TABLE [dbo].[SampleExtraSession] ADD [Id] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'DayId' AND Object_ID = Object_ID(N'SampleExtraSession'))
    BEGIN
            ALTER TABLE [dbo].[SampleExtraSession] ADD [DayId] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'RoomId' AND Object_ID = Object_ID(N'SampleExtraSession'))
    BEGIN
            ALTER TABLE [dbo].[SampleExtraSession] ADD [RoomId] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SessionTitle' AND Object_ID = Object_ID(N'SampleExtraSession'))
    BEGIN
            ALTER TABLE [dbo].[SampleExtraSession] ADD [SessionTitle] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'StartTime' AND Object_ID = Object_ID(N'SampleExtraSession'))
    BEGIN
            ALTER TABLE [dbo].[SampleExtraSession] ADD [StartTime] DATETIME NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'EndTime' AND Object_ID = Object_ID(N'SampleExtraSession'))
    BEGIN
            ALTER TABLE [dbo].[SampleExtraSession] ADD [EndTime] DATETIME NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SessionType' AND Object_ID = Object_ID(N'SampleExtraSession'))
    BEGIN
            ALTER TABLE [dbo].[SampleExtraSession] ADD [SessionType] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'IsCanceled' AND Object_ID = Object_ID(N'SampleExtraSession'))
    BEGIN
            ALTER TABLE [dbo].[SampleExtraSession] ADD [IsCanceled] BIT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'DatumId' AND Object_ID = Object_ID(N'SampleExtraSession'))
    BEGIN
            ALTER TABLE [dbo].[SampleExtraSession] ADD [DatumId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SampleSpeakerAssignmentId' AND Object_ID = Object_ID(N'SampleSpeakerAssignment'))
    BEGIN
            ALTER TABLE [dbo].[SampleSpeakerAssignment] ADD [SampleSpeakerAssignmentId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SpeakerId' AND Object_ID = Object_ID(N'SampleSpeakerAssignment'))
    BEGIN
            ALTER TABLE [dbo].[SampleSpeakerAssignment] ADD [SpeakerId] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SessionId' AND Object_ID = Object_ID(N'SampleSpeakerAssignment'))
    BEGIN
            ALTER TABLE [dbo].[SampleSpeakerAssignment] ADD [SessionId] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'DatumId' AND Object_ID = Object_ID(N'SampleSpeakerAssignment'))
    BEGIN
            ALTER TABLE [dbo].[SampleSpeakerAssignment] ADD [DatumId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SampleAttendanceActionId' AND Object_ID = Object_ID(N'SampleAttendanceAction'))
    BEGIN
            ALTER TABLE [dbo].[SampleAttendanceAction] ADD [SampleAttendanceActionId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Id' AND Object_ID = Object_ID(N'SampleAttendanceAction'))
    BEGIN
            ALTER TABLE [dbo].[SampleAttendanceAction] ADD [Id] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SessionId' AND Object_ID = Object_ID(N'SampleAttendanceAction'))
    BEGIN
            ALTER TABLE [dbo].[SampleAttendanceAction] ADD [SessionId] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'AttendeeId' AND Object_ID = Object_ID(N'SampleAttendanceAction'))
    BEGIN
            ALTER TABLE [dbo].[SampleAttendanceAction] ADD [AttendeeId] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'CheckInTime' AND Object_ID = Object_ID(N'SampleAttendanceAction'))
    BEGIN
            ALTER TABLE [dbo].[SampleAttendanceAction] ADD [CheckInTime] DATETIME NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'DatumId' AND Object_ID = Object_ID(N'SampleAttendanceAction'))
    BEGIN
            ALTER TABLE [dbo].[SampleAttendanceAction] ADD [DatumId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Root-meta-modelId' AND Object_ID = Object_ID(N'Root-meta-model'))
    BEGIN
            ALTER TABLE [dbo].[Root-meta-model] ADD [Root-meta-modelId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Title' AND Object_ID = Object_ID(N'Root-meta-model'))
    BEGIN
            ALTER TABLE [dbo].[Root-meta-model] ADD [Title] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Subtitle' AND Object_ID = Object_ID(N'Root-meta-model'))
    BEGIN
            ALTER TABLE [dbo].[Root-meta-model] ADD [Subtitle] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Date' AND Object_ID = Object_ID(N'Root-meta-model'))
    BEGIN
            ALTER TABLE [dbo].[Root-meta-model] ADD [Date] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Abstract' AND Object_ID = Object_ID(N'Root-meta-model'))
    BEGIN
            ALTER TABLE [dbo].[Root-meta-model] ADD [Abstract] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Meta-modelId' AND Object_ID = Object_ID(N'Root-meta-model'))
    BEGIN
            ALTER TABLE [dbo].[Root-meta-model] ADD [Meta-modelId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'AuthorId' AND Object_ID = Object_ID(N'Author'))
    BEGIN
            ALTER TABLE [dbo].[Author] ADD [AuthorId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Name' AND Object_ID = Object_ID(N'Author'))
    BEGIN
            ALTER TABLE [dbo].[Author] ADD [Name] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Contact' AND Object_ID = Object_ID(N'Author'))
    BEGIN
            ALTER TABLE [dbo].[Author] ADD [Contact] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Affiliations' AND Object_ID = Object_ID(N'Author'))
    BEGIN
            ALTER TABLE [dbo].[Author] ADD [Affiliations] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Root-meta-modelId' AND Object_ID = Object_ID(N'Author'))
    BEGIN
            ALTER TABLE [dbo].[Author] ADD [Root-meta-modelId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'SectionId' AND Object_ID = Object_ID(N'Section'))
    BEGIN
            ALTER TABLE [dbo].[Section] ADD [SectionId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Title' AND Object_ID = Object_ID(N'Section'))
    BEGIN
            ALTER TABLE [dbo].[Section] ADD [Title] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Content' AND Object_ID = Object_ID(N'Section'))
    BEGIN
            ALTER TABLE [dbo].[Section] ADD [Content] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'NarrativeId' AND Object_ID = Object_ID(N'Section'))
    BEGIN
            ALTER TABLE [dbo].[Section] ADD [NarrativeId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'CMCC_ToEMM_Domain_ListId' AND Object_ID = Object_ID(N'CMCC_ToEMM_Domain_List'))
    BEGIN
            ALTER TABLE [dbo].[CMCC_ToEMM_Domain_List] ADD [CMCC_ToEMM_Domain_ListId] INT NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Id' AND Object_ID = Object_ID(N'CMCC_ToEMM_Domain_List'))
    BEGIN
            ALTER TABLE [dbo].[CMCC_ToEMM_Domain_List] ADD [Id] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Fullname' AND Object_ID = Object_ID(N'CMCC_ToEMM_Domain_List'))
    BEGIN
            ALTER TABLE [dbo].[CMCC_ToEMM_Domain_List] ADD [Fullname] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Name' AND Object_ID = Object_ID(N'CMCC_ToEMM_Domain_List'))
    BEGIN
            ALTER TABLE [dbo].[CMCC_ToEMM_Domain_List] ADD [Name] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Description' AND Object_ID = Object_ID(N'CMCC_ToEMM_Domain_List'))
    BEGIN
            ALTER TABLE [dbo].[CMCC_ToEMM_Domain_List] ADD [Description] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Nickname' AND Object_ID = Object_ID(N'CMCC_ToEMM_Domain_List'))
    BEGIN
            ALTER TABLE [dbo].[CMCC_ToEMM_Domain_List] ADD [Nickname] NVARCHAR(100) NULL;
    END

    
    IF NOT EXISTS(SELECT * FROM sys.columns WHERE Name = N'Root-meta-modelId' AND Object_ID = Object_ID(N'CMCC_ToEMM_Domain_List'))
    BEGIN
            ALTER TABLE [dbo].[CMCC_ToEMM_Domain_List] ADD [Root-meta-modelId] INT NULL;
    END

    

              -- ****** KEYS FOR Table [dbo].[JsonWrapper]

              -- ****** KEYS FOR Table [dbo].[Meta-model]
                  -- 
          -- FK for JsonWrapperId :: 4 :: Meta-model :: JsonWrapper
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Meta-model_JsonWrapper]') AND parent_object_id = OBJECT_ID(N'[dbo].[Meta-model]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Meta-model_JsonWrapper]') AND parent_object_id = OBJECT_ID(N'[dbo].[Meta-model]'))
                ALTER TABLE [dbo].[Meta-model]  WITH CHECK ADD  CONSTRAINT [FK_Meta-model_JsonWrapper] FOREIGN KEY([JsonWrapperId])
                    REFERENCES [dbo].[JsonWrapper] (JsonWrapperId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Meta-model_JsonWrapper]') AND parent_object_id = OBJECT_ID(N'[dbo].[Meta-model]'))
            ALTER TABLE [dbo].[Meta-model] CHECK CONSTRAINT [FK_Meta-model_JsonWrapper]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Meta]
                  -- 
          -- FK for Meta-modelId :: 1 :: Meta :: Meta-model
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Meta_Meta-modelIdMeta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Meta]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Meta_Meta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Meta]'))
                ALTER TABLE [dbo].[Meta]  WITH CHECK ADD  CONSTRAINT [FK_Meta_Meta-modelIdMeta-model] FOREIGN KEY([Meta-modelId])
                    REFERENCES [dbo].[Meta-model] (Meta-modelId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Meta_Meta-modelIdMeta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Meta]'))
            ALTER TABLE [dbo].[Meta] CHECK CONSTRAINT [FK_Meta_Meta-modelIdMeta-model]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Executive_summary]
                  -- 
          -- FK for MetaId :: 2 :: Executive_summary :: Meta
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Executive_summary_Meta]') AND parent_object_id = OBJECT_ID(N'[dbo].[Executive_summary]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Executive_summary_Meta]') AND parent_object_id = OBJECT_ID(N'[dbo].[Executive_summary]'))
                ALTER TABLE [dbo].[Executive_summary]  WITH CHECK ADD  CONSTRAINT [FK_Executive_summary_Meta] FOREIGN KEY([MetaId])
                    REFERENCES [dbo].[Meta] (MetaId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Executive_summary_Meta]') AND parent_object_id = OBJECT_ID(N'[dbo].[Executive_summary]'))
            ALTER TABLE [dbo].[Executive_summary] CHECK CONSTRAINT [FK_Executive_summary_Meta]
            GO
          
                  -- 
          -- FK for Root-meta-modelId :: 2 :: Executive_summary :: Root-meta-model
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Executive_summary_Root-meta-modelIdRoot-meta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Executive_summary]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Executive_summary_Root-meta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Executive_summary]'))
                ALTER TABLE [dbo].[Executive_summary]  WITH CHECK ADD  CONSTRAINT [FK_Executive_summary_Root-meta-modelIdRoot-meta-model] FOREIGN KEY([Root-meta-modelId])
                    REFERENCES [dbo].[Root-meta-model] (Root-meta-modelId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Executive_summary_Root-meta-modelIdRoot-meta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Executive_summary]'))
            ALTER TABLE [dbo].[Executive_summary] CHECK CONSTRAINT [FK_Executive_summary_Root-meta-modelIdRoot-meta-model]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Narrative]
                  -- 
          -- FK for Executive_summaryId :: 1 :: Narrative :: Executive_summary
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Narrative_Executive_summaryIdExecutive_summary]') AND parent_object_id = OBJECT_ID(N'[dbo].[Narrative]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Narrative_Executive_summary]') AND parent_object_id = OBJECT_ID(N'[dbo].[Narrative]'))
                ALTER TABLE [dbo].[Narrative]  WITH CHECK ADD  CONSTRAINT [FK_Narrative_Executive_summaryIdExecutive_summary] FOREIGN KEY([Executive_summaryId])
                    REFERENCES [dbo].[Executive_summary] (Executive_summaryId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Narrative_Executive_summaryIdExecutive_summary]') AND parent_object_id = OBJECT_ID(N'[dbo].[Narrative]'))
            ALTER TABLE [dbo].[Narrative] CHECK CONSTRAINT [FK_Narrative_Executive_summaryIdExecutive_summary]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Addressing_concerns_preemptively]
                  -- 
          -- FK for Executive_summaryId :: 0 :: Addressing_concerns_preemptively :: Executive_summary
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Addressing_concerns_preemptively_Executive_summaryIdExecutive_summary]') AND parent_object_id = OBJECT_ID(N'[dbo].[Addressing_concerns_preemptively]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Addressing_concerns_preemptively_Executive_summary]') AND parent_object_id = OBJECT_ID(N'[dbo].[Addressing_concerns_preemptively]'))
                ALTER TABLE [dbo].[Addressing_concerns_preemptively]  WITH CHECK ADD  CONSTRAINT [FK_Addressing_concerns_preemptively_Executive_summaryIdExecutive_summary] FOREIGN KEY([Executive_summaryId])
                    REFERENCES [dbo].[Executive_summary] (Executive_summaryId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Addressing_concerns_preemptively_Executive_summaryIdExecutive_summary]') AND parent_object_id = OBJECT_ID(N'[dbo].[Addressing_concerns_preemptively]'))
            ALTER TABLE [dbo].[Addressing_concerns_preemptively] CHECK CONSTRAINT [FK_Addressing_concerns_preemptively_Executive_summaryIdExecutive_summary]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Schema]
                  -- 
          -- FK for Meta-modelId :: 2 :: Schema :: Meta-model
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Schema_Meta-modelIdMeta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Schema]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Schema_Meta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Schema]'))
                ALTER TABLE [dbo].[Schema]  WITH CHECK ADD  CONSTRAINT [FK_Schema_Meta-modelIdMeta-model] FOREIGN KEY([Meta-modelId])
                    REFERENCES [dbo].[Meta-model] (Meta-modelId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Schema_Meta-modelIdMeta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Schema]'))
            ALTER TABLE [dbo].[Schema] CHECK CONSTRAINT [FK_Schema_Meta-modelIdMeta-model]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Entity]
                  -- 
          -- FK for SchemaId :: 5 :: Entity :: Schema
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Entity_SchemaIdSchema]') AND parent_object_id = OBJECT_ID(N'[dbo].[Entity]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Entity_Schema]') AND parent_object_id = OBJECT_ID(N'[dbo].[Entity]'))
                ALTER TABLE [dbo].[Entity]  WITH CHECK ADD  CONSTRAINT [FK_Entity_SchemaIdSchema] FOREIGN KEY([SchemaId])
                    REFERENCES [dbo].[Schema] (SchemaId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Entity_SchemaIdSchema]') AND parent_object_id = OBJECT_ID(N'[dbo].[Entity]'))
            ALTER TABLE [dbo].[Entity] CHECK CONSTRAINT [FK_Entity_SchemaIdSchema]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Field]
                  -- 
          -- FK for EntityId :: 0 :: Field :: Entity
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Field_EntityIdEntity]') AND parent_object_id = OBJECT_ID(N'[dbo].[Field]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Field_Entity]') AND parent_object_id = OBJECT_ID(N'[dbo].[Field]'))
                ALTER TABLE [dbo].[Field]  WITH CHECK ADD  CONSTRAINT [FK_Field_EntityIdEntity] FOREIGN KEY([EntityId])
                    REFERENCES [dbo].[Entity] (EntityId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Field_EntityIdEntity]') AND parent_object_id = OBJECT_ID(N'[dbo].[Field]'))
            ALTER TABLE [dbo].[Field] CHECK CONSTRAINT [FK_Field_EntityIdEntity]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Lookup]
                  -- 
          -- FK for EntityId :: 0 :: Lookup :: Entity
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Lookup_EntityIdEntity]') AND parent_object_id = OBJECT_ID(N'[dbo].[Lookup]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Lookup_Entity]') AND parent_object_id = OBJECT_ID(N'[dbo].[Lookup]'))
                ALTER TABLE [dbo].[Lookup]  WITH CHECK ADD  CONSTRAINT [FK_Lookup_EntityIdEntity] FOREIGN KEY([EntityId])
                    REFERENCES [dbo].[Entity] (EntityId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Lookup_EntityIdEntity]') AND parent_object_id = OBJECT_ID(N'[dbo].[Lookup]'))
            ALTER TABLE [dbo].[Lookup] CHECK CONSTRAINT [FK_Lookup_EntityIdEntity]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Aggregation]
                  -- 
          -- FK for EntityId :: 0 :: Aggregation :: Entity
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Aggregation_EntityIdEntity]') AND parent_object_id = OBJECT_ID(N'[dbo].[Aggregation]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Aggregation_Entity]') AND parent_object_id = OBJECT_ID(N'[dbo].[Aggregation]'))
                ALTER TABLE [dbo].[Aggregation]  WITH CHECK ADD  CONSTRAINT [FK_Aggregation_EntityIdEntity] FOREIGN KEY([EntityId])
                    REFERENCES [dbo].[Entity] (EntityId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Aggregation_EntityIdEntity]') AND parent_object_id = OBJECT_ID(N'[dbo].[Aggregation]'))
            ALTER TABLE [dbo].[Aggregation] CHECK CONSTRAINT [FK_Aggregation_EntityIdEntity]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Lambda]
                  -- 
          -- FK for EntityId :: 0 :: Lambda :: Entity
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Lambda_EntityIdEntity]') AND parent_object_id = OBJECT_ID(N'[dbo].[Lambda]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Lambda_Entity]') AND parent_object_id = OBJECT_ID(N'[dbo].[Lambda]'))
                ALTER TABLE [dbo].[Lambda]  WITH CHECK ADD  CONSTRAINT [FK_Lambda_EntityIdEntity] FOREIGN KEY([EntityId])
                    REFERENCES [dbo].[Entity] (EntityId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Lambda_EntityIdEntity]') AND parent_object_id = OBJECT_ID(N'[dbo].[Lambda]'))
            ALTER TABLE [dbo].[Lambda] CHECK CONSTRAINT [FK_Lambda_EntityIdEntity]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Constraint]
                  -- 
          -- FK for EntityId :: 0 :: Constraint :: Entity
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Constraint_EntityIdEntity]') AND parent_object_id = OBJECT_ID(N'[dbo].[Constraint]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Constraint_Entity]') AND parent_object_id = OBJECT_ID(N'[dbo].[Constraint]'))
                ALTER TABLE [dbo].[Constraint]  WITH CHECK ADD  CONSTRAINT [FK_Constraint_EntityIdEntity] FOREIGN KEY([EntityId])
                    REFERENCES [dbo].[Entity] (EntityId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Constraint_EntityIdEntity]') AND parent_object_id = OBJECT_ID(N'[dbo].[Constraint]'))
            ALTER TABLE [dbo].[Constraint] CHECK CONSTRAINT [FK_Constraint_EntityIdEntity]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Datum]
                  -- 
          -- FK for SchemaId :: 12 :: Datum :: Schema
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Datum_SchemaIdSchema]') AND parent_object_id = OBJECT_ID(N'[dbo].[Datum]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Datum_Schema]') AND parent_object_id = OBJECT_ID(N'[dbo].[Datum]'))
                ALTER TABLE [dbo].[Datum]  WITH CHECK ADD  CONSTRAINT [FK_Datum_SchemaIdSchema] FOREIGN KEY([SchemaId])
                    REFERENCES [dbo].[Schema] (SchemaId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Datum_SchemaIdSchema]') AND parent_object_id = OBJECT_ID(N'[dbo].[Datum]'))
            ALTER TABLE [dbo].[Datum] CHECK CONSTRAINT [FK_Datum_SchemaIdSchema]
            GO
          
                  -- 
          -- FK for Meta-modelId :: 12 :: Datum :: Meta-model
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Datum_Meta-modelIdMeta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Datum]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Datum_Meta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Datum]'))
                ALTER TABLE [dbo].[Datum]  WITH CHECK ADD  CONSTRAINT [FK_Datum_Meta-modelIdMeta-model] FOREIGN KEY([Meta-modelId])
                    REFERENCES [dbo].[Meta-model] (Meta-modelId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Datum_Meta-modelIdMeta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Datum]'))
            ALTER TABLE [dbo].[Datum] CHECK CONSTRAINT [FK_Datum_Meta-modelIdMeta-model]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Conference]
                  -- 
          -- FK for DatumId :: 0 :: Conference :: Datum
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Conference_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Conference]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Conference_Datum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Conference]'))
                ALTER TABLE [dbo].[Conference]  WITH CHECK ADD  CONSTRAINT [FK_Conference_DatumIdDatum] FOREIGN KEY([DatumId])
                    REFERENCES [dbo].[Datum] (DatumId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Conference_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Conference]'))
            ALTER TABLE [dbo].[Conference] CHECK CONSTRAINT [FK_Conference_DatumIdDatum]
            GO
          

              -- ****** KEYS FOR Table [dbo].[ConferenceDay]
                  -- 
          -- FK for DatumId :: 0 :: ConferenceDay :: Datum
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_ConferenceDay_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[ConferenceDay]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_ConferenceDay_Datum]') AND parent_object_id = OBJECT_ID(N'[dbo].[ConferenceDay]'))
                ALTER TABLE [dbo].[ConferenceDay]  WITH CHECK ADD  CONSTRAINT [FK_ConferenceDay_DatumIdDatum] FOREIGN KEY([DatumId])
                    REFERENCES [dbo].[Datum] (DatumId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_ConferenceDay_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[ConferenceDay]'))
            ALTER TABLE [dbo].[ConferenceDay] CHECK CONSTRAINT [FK_ConferenceDay_DatumIdDatum]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Room]
                  -- 
          -- FK for DatumId :: 0 :: Room :: Datum
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Room_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Room]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Room_Datum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Room]'))
                ALTER TABLE [dbo].[Room]  WITH CHECK ADD  CONSTRAINT [FK_Room_DatumIdDatum] FOREIGN KEY([DatumId])
                    REFERENCES [dbo].[Datum] (DatumId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Room_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Room]'))
            ALTER TABLE [dbo].[Room] CHECK CONSTRAINT [FK_Room_DatumIdDatum]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Session]
                  -- 
          -- FK for DatumId :: 0 :: Session :: Datum
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Session_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Session]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Session_Datum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Session]'))
                ALTER TABLE [dbo].[Session]  WITH CHECK ADD  CONSTRAINT [FK_Session_DatumIdDatum] FOREIGN KEY([DatumId])
                    REFERENCES [dbo].[Datum] (DatumId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Session_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Session]'))
            ALTER TABLE [dbo].[Session] CHECK CONSTRAINT [FK_Session_DatumIdDatum]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Speaker]
                  -- 
          -- FK for DatumId :: 0 :: Speaker :: Datum
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Speaker_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Speaker]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Speaker_Datum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Speaker]'))
                ALTER TABLE [dbo].[Speaker]  WITH CHECK ADD  CONSTRAINT [FK_Speaker_DatumIdDatum] FOREIGN KEY([DatumId])
                    REFERENCES [dbo].[Datum] (DatumId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Speaker_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Speaker]'))
            ALTER TABLE [dbo].[Speaker] CHECK CONSTRAINT [FK_Speaker_DatumIdDatum]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Attendee]
                  -- 
          -- FK for DatumId :: 0 :: Attendee :: Datum
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Attendee_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Attendee]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Attendee_Datum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Attendee]'))
                ALTER TABLE [dbo].[Attendee]  WITH CHECK ADD  CONSTRAINT [FK_Attendee_DatumIdDatum] FOREIGN KEY([DatumId])
                    REFERENCES [dbo].[Datum] (DatumId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Attendee_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Attendee]'))
            ALTER TABLE [dbo].[Attendee] CHECK CONSTRAINT [FK_Attendee_DatumIdDatum]
            GO
          

              -- ****** KEYS FOR Table [dbo].[SessionAttendanceEvent]
                  -- 
          -- FK for DatumId :: 0 :: SessionAttendanceEvent :: Datum
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_SessionAttendanceEvent_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[SessionAttendanceEvent]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_SessionAttendanceEvent_Datum]') AND parent_object_id = OBJECT_ID(N'[dbo].[SessionAttendanceEvent]'))
                ALTER TABLE [dbo].[SessionAttendanceEvent]  WITH CHECK ADD  CONSTRAINT [FK_SessionAttendanceEvent_DatumIdDatum] FOREIGN KEY([DatumId])
                    REFERENCES [dbo].[Datum] (DatumId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_SessionAttendanceEvent_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[SessionAttendanceEvent]'))
            ALTER TABLE [dbo].[SessionAttendanceEvent] CHECK CONSTRAINT [FK_SessionAttendanceEvent_DatumIdDatum]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Sponsor]
                  -- 
          -- FK for DatumId :: 0 :: Sponsor :: Datum
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Sponsor_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Sponsor]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Sponsor_Datum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Sponsor]'))
                ALTER TABLE [dbo].[Sponsor]  WITH CHECK ADD  CONSTRAINT [FK_Sponsor_DatumIdDatum] FOREIGN KEY([DatumId])
                    REFERENCES [dbo].[Datum] (DatumId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Sponsor_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[Sponsor]'))
            ALTER TABLE [dbo].[Sponsor] CHECK CONSTRAINT [FK_Sponsor_DatumIdDatum]
            GO
          

              -- ****** KEYS FOR Table [dbo].[ConferencePolicy]
                  -- 
          -- FK for DatumId :: 0 :: ConferencePolicy :: Datum
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_ConferencePolicy_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[ConferencePolicy]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_ConferencePolicy_Datum]') AND parent_object_id = OBJECT_ID(N'[dbo].[ConferencePolicy]'))
                ALTER TABLE [dbo].[ConferencePolicy]  WITH CHECK ADD  CONSTRAINT [FK_ConferencePolicy_DatumIdDatum] FOREIGN KEY([DatumId])
                    REFERENCES [dbo].[Datum] (DatumId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_ConferencePolicy_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[ConferencePolicy]'))
            ALTER TABLE [dbo].[ConferencePolicy] CHECK CONSTRAINT [FK_ConferencePolicy_DatumIdDatum]
            GO
          

              -- ****** KEYS FOR Table [dbo].[SampleExtraSession]
                  -- 
          -- FK for DatumId :: 0 :: SampleExtraSession :: Datum
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_SampleExtraSession_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[SampleExtraSession]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_SampleExtraSession_Datum]') AND parent_object_id = OBJECT_ID(N'[dbo].[SampleExtraSession]'))
                ALTER TABLE [dbo].[SampleExtraSession]  WITH CHECK ADD  CONSTRAINT [FK_SampleExtraSession_DatumIdDatum] FOREIGN KEY([DatumId])
                    REFERENCES [dbo].[Datum] (DatumId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_SampleExtraSession_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[SampleExtraSession]'))
            ALTER TABLE [dbo].[SampleExtraSession] CHECK CONSTRAINT [FK_SampleExtraSession_DatumIdDatum]
            GO
          

              -- ****** KEYS FOR Table [dbo].[SampleSpeakerAssignment]
                  -- 
          -- FK for DatumId :: 0 :: SampleSpeakerAssignment :: Datum
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_SampleSpeakerAssignment_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[SampleSpeakerAssignment]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_SampleSpeakerAssignment_Datum]') AND parent_object_id = OBJECT_ID(N'[dbo].[SampleSpeakerAssignment]'))
                ALTER TABLE [dbo].[SampleSpeakerAssignment]  WITH CHECK ADD  CONSTRAINT [FK_SampleSpeakerAssignment_DatumIdDatum] FOREIGN KEY([DatumId])
                    REFERENCES [dbo].[Datum] (DatumId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_SampleSpeakerAssignment_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[SampleSpeakerAssignment]'))
            ALTER TABLE [dbo].[SampleSpeakerAssignment] CHECK CONSTRAINT [FK_SampleSpeakerAssignment_DatumIdDatum]
            GO
          

              -- ****** KEYS FOR Table [dbo].[SampleAttendanceAction]
                  -- 
          -- FK for DatumId :: 0 :: SampleAttendanceAction :: Datum
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_SampleAttendanceAction_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[SampleAttendanceAction]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_SampleAttendanceAction_Datum]') AND parent_object_id = OBJECT_ID(N'[dbo].[SampleAttendanceAction]'))
                ALTER TABLE [dbo].[SampleAttendanceAction]  WITH CHECK ADD  CONSTRAINT [FK_SampleAttendanceAction_DatumIdDatum] FOREIGN KEY([DatumId])
                    REFERENCES [dbo].[Datum] (DatumId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_SampleAttendanceAction_DatumIdDatum]') AND parent_object_id = OBJECT_ID(N'[dbo].[SampleAttendanceAction]'))
            ALTER TABLE [dbo].[SampleAttendanceAction] CHECK CONSTRAINT [FK_SampleAttendanceAction_DatumIdDatum]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Root-meta-model]
                  -- 
          -- FK for Meta-modelId :: 3 :: Root-meta-model :: Meta-model
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Root-meta-model_Meta-modelIdMeta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Root-meta-model]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Root-meta-model_Meta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Root-meta-model]'))
                ALTER TABLE [dbo].[Root-meta-model]  WITH CHECK ADD  CONSTRAINT [FK_Root-meta-model_Meta-modelIdMeta-model] FOREIGN KEY([Meta-modelId])
                    REFERENCES [dbo].[Meta-model] (Meta-modelId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Root-meta-model_Meta-modelIdMeta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Root-meta-model]'))
            ALTER TABLE [dbo].[Root-meta-model] CHECK CONSTRAINT [FK_Root-meta-model_Meta-modelIdMeta-model]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Author]
                  -- 
          -- FK for Root-meta-modelId :: 0 :: Author :: Root-meta-model
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Author_Root-meta-modelIdRoot-meta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Author]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Author_Root-meta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Author]'))
                ALTER TABLE [dbo].[Author]  WITH CHECK ADD  CONSTRAINT [FK_Author_Root-meta-modelIdRoot-meta-model] FOREIGN KEY([Root-meta-modelId])
                    REFERENCES [dbo].[Root-meta-model] (Root-meta-modelId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Author_Root-meta-modelIdRoot-meta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[Author]'))
            ALTER TABLE [dbo].[Author] CHECK CONSTRAINT [FK_Author_Root-meta-modelIdRoot-meta-model]
            GO
          

              -- ****** KEYS FOR Table [dbo].[Section]
                  -- 
          -- FK for NarrativeId :: 0 :: Section :: Narrative
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Section_Narrative]') AND parent_object_id = OBJECT_ID(N'[dbo].[Section]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Section_Narrative]') AND parent_object_id = OBJECT_ID(N'[dbo].[Section]'))
                ALTER TABLE [dbo].[Section]  WITH CHECK ADD  CONSTRAINT [FK_Section_Narrative] FOREIGN KEY([NarrativeId])
                    REFERENCES [dbo].[Narrative] (NarrativeId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_Section_Narrative]') AND parent_object_id = OBJECT_ID(N'[dbo].[Section]'))
            ALTER TABLE [dbo].[Section] CHECK CONSTRAINT [FK_Section_Narrative]
            GO
          

              -- ****** KEYS FOR Table [dbo].[CMCC_ToEMM_Domain_List]
                  -- 
          -- FK for Root-meta-modelId :: 0 :: CMCC_ToEMM_Domain_List :: Root-meta-model
          IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_CMCC_ToEMM_Domain_List_Root-meta-modelIdRoot-meta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[CMCC_ToEMM_Domain_List]'))
              IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_CMCC_ToEMM_Domain_List_Root-meta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[CMCC_ToEMM_Domain_List]'))
                ALTER TABLE [dbo].[CMCC_ToEMM_Domain_List]  WITH CHECK ADD  CONSTRAINT [FK_CMCC_ToEMM_Domain_List_Root-meta-modelIdRoot-meta-model] FOREIGN KEY([Root-meta-modelId])
                    REFERENCES [dbo].[Root-meta-model] (Root-meta-modelId)
                GO

          IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_CMCC_ToEMM_Domain_List_Root-meta-modelIdRoot-meta-model]') AND parent_object_id = OBJECT_ID(N'[dbo].[CMCC_ToEMM_Domain_List]'))
            ALTER TABLE [dbo].[CMCC_ToEMM_Domain_List] CHECK CONSTRAINT [FK_CMCC_ToEMM_Domain_List_Root-meta-modelIdRoot-meta-model]
            GO
          


            SELECT 'Successful' as Value
            FROM (SELECT NULL AS FIELD) as Result
            FOR XML AUTO

          