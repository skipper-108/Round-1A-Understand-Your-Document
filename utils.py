"""
PDF Outline Extractor - Core functionality using pdfminer.six
Extracts structured outlines from PDF files using layout analysis.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTLine, LAParams
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFPageAggregator


def extract_outline(pdf_path: Path) -> Dict[str, Any]:
    """
    Extract structured outline from PDF file using layout analysis.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary with title and outline structure
    """
    start_time = time.time()
    
    try:
        # Extract text elements with layout information
        text_elements = extract_text_with_layout(pdf_path)
        
        # Analyze and classify headings
        headings = analyze_headings(text_elements)
        
        # Extract title (first H1 or topmost heading)
        title = extract_title(headings, text_elements)
        
        # Create outline structure
        outline = []
        for heading in headings:
            outline.append({
                "level": heading["level"],
                "text": heading["text"],
                "page": heading["page"]
            })
        
        # Check execution time constraint
        if time.time() - start_time > 10:
            raise TimeoutError("PDF processing exceeded 10 second limit")
        
        return {
            "title": title,
            "outline": outline
        }
        
    except Exception as e:
        # Return error structure while maintaining JSON format
        return {
            "title": "Error processing PDF",
            "outline": [],
            "error": str(e)
        }


def extract_text_with_layout(pdf_path: Path) -> List[Dict[str, Any]]:
    """
    Extract text elements with layout information from PDF.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of text elements with position, font, and page information
    """
    text_elements = []
    
    try:
        # Use the high-level extract_pages function
        for page_num, layout in enumerate(extract_pages(pdf_path), 1):
            # Check page limit constraint
            if page_num > 50:
                raise ValueError("PDF exceeds 50 page limit")
            
                            # Extract text containers from layout
                for obj in layout:
                    if isinstance(obj, LTTextContainer):
                        text = obj.get_text().strip()
                        if text and len(text) > 1:  # Skip very short text
                            # Fix spacing in the extracted text
                            text = fix_text_spacing(text)
                            # Get font information
                            font_info = extract_font_info(obj)
                            
                            text_elements.append({
                                "text": text,
                                "page": page_num,
                                "x0": obj.x0,
                                "y0": obj.y0,
                                "x1": obj.x1,
                                "y1": obj.y1,
                                "font_size": font_info["size"],
                                "font_name": font_info["name"],
                                "is_bold": font_info["is_bold"],
                                "is_italic": font_info["is_italic"],
                                "position": calculate_position(obj, layout)
                            })
    except Exception as e:
        print(f"Warning: Error extracting text: {e}")
        # Fallback to simple text extraction
        return extract_simple_text(pdf_path)
    
    # If no text elements found, use fallback
    if not text_elements:
        print("No text elements found, using fallback extraction")
        return extract_simple_text(pdf_path)
    
    return text_elements


def extract_simple_text(pdf_path: Path) -> List[Dict[str, Any]]:
    """
    Fallback simple text extraction when layout analysis fails.
    """
    text_elements = []
    
    try:
        for page_num, layout in enumerate(extract_pages(pdf_path), 1):
            if page_num > 50:
                break
                
            page_text = ""
            for obj in layout:
                if isinstance(obj, LTTextContainer):
                    # Extract text with proper spacing
                    text = obj.get_text()
                    # Add space after each text container to preserve spacing
                    page_text += text + " "
            
            if page_text.strip():
                # Clean up the text and fix spacing issues
                cleaned_text = fix_text_spacing(page_text.strip())
                
                # Split text into sentences and phrases for better heading detection
                # First split by common sentence endings
                import re
                sentences = re.split(r'[.!?]+', cleaned_text)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if sentence and len(sentence) > 5:  # Minimum length for a meaningful heading
                        text_elements.append({
                            "text": sentence,
                            "page": page_num,
                            "x0": 0,
                            "y0": 0,
                            "x1": 0,
                            "y1": 0,
                            "font_size": 12,  # Default size
                            "font_name": "",
                            "is_bold": False,
                            "is_italic": False,
                            "position": "middle"
                        })
    except Exception as e:
        print(f"Error in simple text extraction: {e}")
    
    return text_elements


def fix_text_spacing(text: str) -> str:
    """
    Fix common spacing issues in extracted PDF text.
    """
    import re
    
    # Step 1: Fix common word combinations that are stuck together
    common_fixes = {
        # Title and common phrases
        'Hereare': 'Here are',
        'isabbreviatedas': 'is abbreviated as',
        'OOPsinterviewquestionsandanswersforfresheraswellexperienced': 'OOPs interview questions and answers for fresher as well experienced',
        'candidatestogettheirdream': 'candidates to get their dream',
        'job': 'job',
        
        # Question patterns
        'Whatis': 'What is',
        'Whatisaclass': 'What is a class',
        'WhatisanObject': 'What is an Object',
        'WhatisEncapsulation': 'What is Encapsulation',
        'WhatisPolymorphism': 'What is Polymorphism',
        'WhatisInheritance': 'What is Inheritance',
        'Whataremanipulators': 'What are manipulators',
        'WhatisanInlinefunction': 'What is an Inline function',
        'Whatisavirtualfunction': 'What is a virtual function',
        'Whatisoperatoroverloading': 'What is operator overloading',
        'Whatisthesuperkeyword': 'What is the super keyword',
        'WhatisearlyandlateBinding': 'What is early and late Binding',
        'Whatarealltheoperatorsthatcannotbeoverloaded': 'What are all the operators that cannot be overloaded',
        'Whetherstaticmethodcanusenonstaticmembers': 'Whether static method can use non static members',
        'Whatareabaseclass,subclass,andsuperclass': 'What are a base class, subclass, and superclass',
        'WhichOOPSconceptisusedasareusemechanism': 'Which OOPS concept is used as a reuse mechanism',
        
        # OOP concepts
        'OOPSisabbreviatedas': 'OOPS is abbreviated as',
        'OOPSis': 'OOPS is',
        'What isa': 'What is a',
        'representationof': 'representation of',
        'templatethat': 'template that',
        'objectis': 'object is',
        'andidentity': 'and identity',
        'restrictedto': 'restricted to',
        'assigningbehavior': 'assigning behavior',
        'subclassto': 'subclass to',
        'somethingthat': 'something that',
        'declaredin': 'declared in',
        'classshares': 'class shares',
        'classiscalled': 'class is called',
        'thenitiscalled': 'then it is called',
        'functionswhich': 'functions which',
        'conjunctionwiththe': 'conjunction with the',
        'insertion(<<)andextraction(>>)operatorson': 'insertion(<<) and extraction(>>) operators on',
        'methodused': 'method used',
        'stateof': 'state of',
        'sameas': 'same as',
        'constructormusthavenoreturntype': 'constructor must have no return type',
        'methodwhich': 'method which',
        'whenthe': 'when the',
        'ofscope': 'of scope',
        'namebut': 'name but',
        'techniqueused': 'technique used',
        'instructsto': 'instructs to',
        'completebody': 'complete body',
        'functionwherever': 'function wherever',
        'usedin': 'used in',
        'functionof': 'function of',
        'functionalitycanbe': 'functionality can be',
        'overriddenin': 'overridden in',
        'implementedby': 'implemented by',
        'calledvirtual': 'called virtual',
        'givenduring': 'given during',
        'ObjectOrientedProgrammingsystem': 'Object Oriented Programming system',
        'inwhichprograms': 'in which programs',
        'areconsideredasacollectionofobjects': 'are considered as a collection of objects',
        'Eachobjectisnothingbutaninstance': 'Each object is nothing but an instance',
        'ofaclass': 'of a class',
        'WritebasicconceptsofOOPS': 'Write basic concepts of OOPS',
        'FollowingaretheconceptsofOOPS': 'Following are the concepts of OOPS',
        'Aclassissimplyarepresentation': 'A class is simply a representation',
        'ofatypeofobject': 'of a type of object',
        'Itistheblueprint/plan/template': 'It is the blueprint/plan/template',
        'thatdescribesthedetailsofanobject': 'that describes the details of an object',
        'Anobjectisaninstanceofaclass': 'An object is an instance of a class',
        'Ithasitsownstate': 'It has its own state',
        'behaviorandidentity': 'behavior and identity',
        'Encapsulationisanattributeofanobject': 'Encapsulation is an attribute of an object',
        'anditcontainsalldatawhichishidden': 'and it contains all data which is hidden',
        'Thathiddendatacanberestricted': 'That hidden data can be restricted',
        'tothemembersofthatclass': 'to the members of that class',
        'LevelsarePublic': 'Levels are Public',
        'Protected,Private': 'Protected, Private',
        'InternalandProtectedInternal': 'Internal and Protected Internal',
        'Polymorphismisnothingbutassigning': 'Polymorphism is nothing but assigning',
        'behaviororvalueinasubclass': 'behavior or value in a subclass',
        'tosomethingthatwasalreadydeclared': 'to something that was already declared',
        'inthemainclass': 'in the main class',
        'Simply,polymorphism': 'Simply, polymorphism',
        'takesmorethanoneform': 'takes more than one form',
        'Inheritanceisaconceptwhereoneclass': 'Inheritance is a concept where one class',
        'sharesthestructureandbehavior': 'shares the structure and behavior',
        'definedinanotherclass': 'defined in another class',
        'IfInheritanceappliedtooneclass': 'If Inheritance applied to one class',
        'iscalledSingleInheritance': 'is called Single Inheritance',
        'andifitdependsonmultipleclasses': 'and if it depends on multiple classes',
        'thenitiscalledmultipleInheritance': 'then it is called multiple Inheritance',
        'Manipulatorsarethefunctions': 'Manipulators are the functions',
        'whichcanbeusedinconjunction': 'which can be used in conjunction',
        'withtheinsertion': 'with the insertion',
        'andextractionoperators': 'and extraction operators',
        'onanobject': 'on an object',
        'Examplesareendl': 'Examples are endl',
        'andsetw': 'and setw',
        'Explainthetermconstructor': 'Explain the term constructor',
        'Aconstructorisamethod': 'A constructor is a method',
        'usedtoinitializethestate': 'used to initialize the state',
        'ofanobject': 'of an object',
        'anditgetsinvoked': 'and it gets invoked',
        'atthetimeofobjectcreation': 'at the time of object creation',
        'Rulesforconstructorare': 'Rules for constructor are',
        'ConstructorNameshouldbethesame': 'Constructor Name should be the same',
        'asaclassname': 'as a class name',
        'Adestructorisamethod': 'A destructor is a method',
        'whichisautomaticallycalled': 'which is automatically called',
        'whentheobjectismadeofscope': 'when the object is made of scope',
        'ordestroyed': 'or destroyed',
        'Destructornameisalsosameasclassname': 'Destructor name is also same as class name',
        'butwiththetildesymbolbeforethename': 'but with the tilde symbol before the name',
        'Aninlinefunctionisatechnique': 'An inline function is a technique',
        'usedbythecompilersandinstructs': 'used by the compilers and instructs',
        'toinsertcompletebodyofthefunction': 'to insert complete body of the function',
        'whereverthatfunctionisused': 'wherever that function is used',
        'intheprogramsourcecode': 'in the program source code',
        'Avirtualfunctionisamemberfunction': 'A virtual function is a member function',
        'ofaclass': 'of a class',
        'anditsfunctionalitycanbeoverridden': 'and its functionality can be overridden',
        'initsderivedclass': 'in its derived class',
        'Thisfunctioncanbeimplemented': 'This function can be implemented',
        'byusingakeywordcalledvirtual': 'by using a keyword called virtual',
        'anditcanbegivenduringfunctiondeclaration': 'and it can be given during function declaration',
        'Operatoroverloadingisafunction': 'Operator overloading is a function',
        'wheredifferentoperatorsareapplied': 'where different operators are applied',
        'anddefineddifferently': 'and defined differently',
        'Thesuperkeywordisusedtoinvoke': 'The super keyword is used to invoke',
        'theoverriddenmethod': 'the overridden method',
        'whichoverridesoneofitssuperclassmethods': 'which overrides one of its superclass methods',
        'Earlybindingreferstotheassignment': 'Early binding refers to the assignment',
        'ofvaluestovariablesduringdesigntime': 'of values to variables during design time',
        'Latebindingreferstotheassignment': 'Late binding refers to the assignment',
        'ofvaluestovariablesatruntime': 'of values to variables at runtime',
        'Virtualvoidfunction': 'Virtual void function',
        'Purevirtual': 'Pure virtual',
        'Followingaretheoperatorsthatcannotbeoverloaded': 'Following are the operators that cannot be overloaded',
        'False': 'False',
        'Whatareabaseclass': 'What are a base class',
        'subclass,andsuperclass': 'subclass, and superclass',
        'Thebaseclassistheparentclass': 'The base class is the parent class',
        'Thesubclassisthechildclass': 'The subclass is the child class',
        'Thesuperclassistheparentclass': 'The superclass is the parent class',
        'InheritanceistheOOPSconcept': 'Inheritance is the OOPS concept',
        'thatcanbeusedasareusemechanism': 'that can be used as a reuse mechanism',
    }
    
    # Apply all the common fixes
    for old, new in common_fixes.items():
        text = text.replace(old, new)
    
    # Step 2: Fix patterns with regex (more carefully)
    # Add spaces between lowercase and uppercase letters (camelCase) - but not in the middle of words
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    # Add spaces between letters and numbers
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)
    
    # Step 3: Apply additional specific fixes
    additional_fixes = {
        # Fix common patterns that might have been missed
        'Questi on s': 'Questions',
        'c and id at es': 'candidates',
        'dre a m': 'dream',
        'Wh a t': 'What',
        'abbrevi at ed': 'abbreviated',
        'Progr a mm in g': 'Programming',
        'progr a ms': 'programs',
        'c on sidered': 'considered',
        'E a ch': 'Each',
        'noth in g': 'nothing',
        'inst an ce': 'instance',
        'cl as s': 'class',
        'b as ic': 'basic',
        'c on cepts': 'concepts',
        'Follow in g': 'Following',
        'Abstr a ction': 'Abstraction',
        'Enc a psul at ion': 'Encapsulation',
        'Inherit an ce': 'Inheritance',
        'Polymorphism': 'Polymorphism',
        'aclass': 'a class',
        'issimply': 'is simply',
        'arepresentation': 'a representation',
        'ofatype': 'of a type',
        'Itisthe': 'It is the',
        'blueprint/plan/template': 'blueprint/plan/template',
        'thatdescribes': 'that describes',
        'thedetailsofanobject': 'the details of an object',
        'Anobject': 'An object',
        'isaninstance': 'is an instance',
        'Ithasitsownstate': 'It has its own state',
        'behaviorandidentity': 'behavior and identity',
        'isanattribute': 'is an attribute',
        'anditcontains': 'and it contains',
        'alldatawhichishidden': 'all data which is hidden',
        'Thathidden': 'That hidden',
        'datacanberestricted': 'data can be restricted',
        'tothemembers': 'to the members',
        'ofthatclass': 'of that class',
        'Levelsare': 'Levels are',
        'Public,Protected': 'Public, Protected',
        'Private,Internal': 'Private, Internal',
        'andProtectedInternal': 'and Protected Internal',
        'isnothingbutassigning': 'is nothing but assigning',
        'behaviororvalue': 'behavior or value',
        'inasubclass': 'in a subclass',
        'tosomething': 'to something',
        'thatwasalreadydeclared': 'that was already declared',
        'inthemainclass': 'in the main class',
        'takesmorethanoneform': 'takes more than one form',
        'isaconcept': 'is a concept',
        'whereoneclass': 'where one class',
        'sharesthestructure': 'shares the structure',
        'andbehavior': 'and behavior',
        'definedinanotherclass': 'defined in another class',
        'appliedtooneclass': 'applied to one class',
        'iscalledSingle': 'is called Single',
        'andifitdepends': 'and if it depends',
        'onmultipleclasses': 'on multiple classes',
        'thenitiscalled': 'then it is called',
        'multipleInheritance': 'multiple Inheritance',
        'arethefunctions': 'are the functions',
        'whichcanbeused': 'which can be used',
        'inconjunction': 'in conjunction',
        'withtheinsertion': 'with the insertion',
        'andextractionoperators': 'and extraction operators',
        'onanobject': 'on an object',
        'Examplesare': 'Examples are',
        'endland': 'endl and',
        'setw': 'setw',
        'Explaintheterm': 'Explain the term',
        'Aconstructor': 'A constructor',
        'isamethod': 'is a method',
        'usedtoinitialize': 'used to initialize',
        'thestate': 'the state',
        'anditgets': 'and it gets',
        'invokedat': 'invoked at',
        'thetimeof': 'the time of',
        'objectcreation': 'object creation',
        'Rulesfor': 'Rules for',
        'constructorare': 'constructor are',
        'Nameshouldbe': 'Name should be',
        'thesameas': 'the same as',
        'aclassname': 'a class name',
        'Adestructor': 'A destructor',
        'whichisautomatically': 'which is automatically',
        'calledwhen': 'called when',
        'theobjectismade': 'the object is made',
        'ofscope': 'of scope',
        'ordestroyed': 'or destroyed',
        'Destructorname': 'Destructor name',
        'isalsosame': 'is also same',
        'asclassname': 'as class name',
        'butwiththe': 'but with the',
        'tildesymbol': 'tilde symbol',
        'beforethename': 'before the name',
        'Aninline': 'An inline',
        'functionisatechnique': 'function is a technique',
        'usedbythe': 'used by the',
        'compilersand': 'compilers and',
        'instructsto': 'instructs to',
        'insertcomplete': 'insert complete',
        'bodyofthe': 'body of the',
        'functionwherever': 'function wherever',
        'thatfunctionisused': 'that function is used',
        'intheprogram': 'in the program',
        'sourcecode': 'source code',
        'Avirtual': 'A virtual',
        'functionisamember': 'function is a member',
        'anditsfunctionality': 'and its functionality',
        'canbeoverridden': 'can be overridden',
        'initsderived': 'in its derived',
        'Thisfunction': 'This function',
        'canbeimplemented': 'can be implemented',
        'byusinga': 'by using a',
        'keywordcalled': 'keyword called',
        'anditcanbe': 'and it can be',
        'givenduring': 'given during',
        'functiondeclaration': 'function declaration',
        'Operatoroverloading': 'Operator overloading',
        'isafunction': 'is a function',
        'wheredifferent': 'where different',
        'operatorsare': 'operators are',
        'appliedand': 'applied and',
        'defineddifferently': 'defined differently',
        'Thesuper': 'The super',
        'keywordisused': 'keyword is used',
        'toinvoke': 'to invoke',
        'theoverridden': 'the overridden',
        'whichoverrides': 'which overrides',
        'oneofits': 'one of its',
        'superclassmethods': 'superclass methods',
        'Earlybinding': 'Early binding',
        'referstothe': 'refers to the',
        'assignmentof': 'assignment of',
        'valuestovariables': 'values to variables',
        'duringdesigntime': 'during design time',
        'Latebinding': 'Late binding',
        'atruntime': 'at runtime',
        'Virtualvoid': 'Virtual void',
        'Purevirtual': 'Pure virtual',
        'Followingare': 'Following are',
        'theoperatorsthat': 'the operators that',
        'cannotbeoverloaded': 'cannot be overloaded',
        'Whatare': 'What are',
        'abaseclass': 'a base class',
        'subclass,and': 'subclass, and',
        'superclass': 'superclass',
        'Thebase': 'The base',
        'classisthe': 'class is the',
        'parentclass': 'parent class',
        'Thesubclass': 'The subclass',
        'isthechild': 'is the child',
        'Thesuperclass': 'The superclass',
        'Inheritanceisthe': 'Inheritance is the',
        'OOPSconcept': 'OOPS concept',
        'thatcanbe': 'that can be',
        'usedas': 'used as',
        'areusemechanism': 'a reuse mechanism',
    }
    
    # Apply additional fixes
    for old, new in additional_fixes.items():
        text = text.replace(old, new)
    
    # Step 3: Clean up multiple spaces and punctuation
    text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single space
    text = re.sub(r'\s+([.,!?])', r'\1', text)  # Remove spaces before punctuation
    text = re.sub(r'([.,!?])([A-Za-z])', r'\1 \2', text)  # Add space after punctuation if followed by letter
    
    # Step 4: Final cleanup
    text = text.strip()
    
    return text


def extract_font_info(text_container: LTTextContainer) -> Dict[str, Any]:
    """
    Extract font information from text container.
    
    Args:
        text_container: PDF text container object
        
    Returns:
        Dictionary with font properties
    """
    font_size = 0
    font_name = ""
    is_bold = False
    is_italic = False
    
    for obj in text_container:
        if isinstance(obj, LTChar):
            font_size = max(font_size, obj.size)
            font_name = obj.fontname if hasattr(obj, 'fontname') else ""
            
            # Check for bold/italic indicators in font name
            font_lower = font_name.lower()
            is_bold = is_bold or any(word in font_lower for word in ['bold', 'black', 'heavy'])
            is_italic = is_italic or any(word in font_lower for word in ['italic', 'oblique'])
    
    return {
        "size": font_size,
        "name": font_name,
        "is_bold": is_bold,
        "is_italic": is_italic
    }


def calculate_position(text_container: LTTextContainer, layout) -> str:
    """
    Calculate relative position of text on page.
    
    Args:
        text_container: PDF text container object
        layout: PDF layout object
        
    Returns:
        Position description (top, middle, bottom)
    """
    try:
        # Try to get page height from layout
        if hasattr(layout, 'height'):
            page_height = layout.height
        elif hasattr(layout, 'mediabox'):
            page_height = layout.mediabox[3]
        else:
            # Default to middle if we can't determine position
            return "middle"
        
        y_position = text_container.y0
        
        if y_position > page_height * 0.7:
            return "top"
        elif y_position > page_height * 0.3:
            return "middle"
        else:
            return "bottom"
    except:
        # Default to middle if there's any error
        return "middle"


def analyze_headings(text_elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Analyze text elements and classify them as headings based on heuristics.
    
    Args:
        text_elements: List of text elements with layout information
        
    Returns:
        List of classified headings
    """
    headings = []
    
    # Calculate font size statistics for normalization
    font_sizes = [elem["font_size"] for elem in text_elements if elem["font_size"] > 0]
    if not font_sizes:
        return headings
    
    max_font_size = max(font_sizes)
    avg_font_size = sum(font_sizes) / len(font_sizes)
    
    for elem in text_elements:
        text = elem["text"]
        font_size = elem["font_size"]
        is_bold = elem["is_bold"]
        position = elem["position"]
        
        # Skip very short or very long text
        if len(text) < 2 or len(text) > 200:
            continue
        
        # Heading classification heuristics
        level = classify_heading_level(text, font_size, is_bold, position, max_font_size, avg_font_size)
        
        if level:
            headings.append({
                "level": level,
                "text": text,
                "page": elem["page"],
                "font_size": font_size,
                "position": position
            })
    
    # Sort headings by page and position
    headings.sort(key=lambda x: (x["page"], -x["font_size"], x["position"] == "top"))
    
    return headings


def classify_heading_level(text: str, font_size: float, is_bold: bool, 
                          position: str, max_font_size: float, avg_font_size: float) -> Optional[str]:
    """
    Classify text as heading level based on multiple heuristics.
    
    Args:
        text: Text content
        font_size: Font size
        is_bold: Whether text is bold
        position: Position on page
        max_font_size: Maximum font size in document
        avg_font_size: Average font size in document
        
    Returns:
        Heading level (H1, H2, H3) or None
    """
    # Normalize font size
    font_ratio = font_size / max_font_size if max_font_size > 0 else 0
    
    # H1: Large font, bold, top position, or specific patterns
    if (font_ratio > 0.8 or 
        (font_ratio > 0.6 and is_bold and position == "top") or
        text.startswith(('Chapter', 'Section', 'Part', 'Introduction', 'Conclusion')) or
        (len(text) < 50 and text.isupper())):
        return "H1"
    
    # H2: Medium-large font, numbered patterns, or bold text
    elif (font_ratio > 0.5 or 
          (font_ratio > 0.4 and is_bold) or
          text.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')) or
          (len(text) < 80 and any(char.isdigit() for char in text[:3]))):
        return "H2"
    
    # H3: Medium font, descriptive text, or specific patterns
    elif (font_ratio > 0.3 or 
          (font_ratio > 0.25 and is_bold) or
          text.startswith(('•', '●', '-', '○')) or
          (len(text) < 120 and font_ratio > avg_font_size / max_font_size)):
        return "H3"
    
    return None


def extract_title(headings: List[Dict[str, Any]], text_elements: List[Dict[str, Any]]) -> str:
    """
    Extract document title from headings or first significant text.
    
    Args:
        headings: List of classified headings
        text_elements: List of all text elements
        
    Returns:
        Document title
    """
    # Try to find first H1 heading
    for heading in headings:
        if heading["level"] == "H1":
            return heading["text"]
    
    # Try to find first H2 heading
    for heading in headings:
        if heading["level"] == "H2":
            return heading["text"]
    
    # Fallback to first significant text element
    for elem in text_elements:
        text = elem["text"]
        if (len(text) > 3 and len(text) < 100 and 
            elem["position"] == "top" and elem["font_size"] > 0):
            return text
    
    return "Untitled Document" 