# nodes.py
"""Implementation of workflow nodes for the support agent."""
from PIL import Image
from typing import Dict, Any
from transformers import TextStreamer

from schemas import SomeState

class NodeFunctions:
    """Collection of node functions used in the workflow graph."""
    
    def __init__(self, models: Dict[str, Any]):
        """
        Initialize with required models.
        
        Args:
            models: Dictionary containing all required models
        """
        self.classifier_llm = models.get("classifier_llm")
        self.agent_conversation_llm = models.get("agent_conversation_llm")
        self.agent_conversation_chain = models.get("agent_conversation_chain")
        self.ov_model = models.get("ov_model")
        self.processor = models.get("processor")
    
    def classifier(self, state: SomeState) -> dict:
        """
        Classify user complaint as refundable or non-refundable.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with classification
        """
        print("\n[Node: classifier]")
        user_message = state.get("user_message", "")
        
        prompt = f"""
                Classify the following user complaint as either 'refundable' or 'non_refundable'.  
                The complaint: "{user_message}"  

                ### **Rules for Classification**  

                #### **Refundable Issues** (Respond with 'refundable')  
                A complaint is **refundable** if it involves any of the following:  
                - The item **arrived damaged** (e.g., torn packaging, broken container, spilled liquid).  
                - The item **arrived cold** when it should have been hot (e.g., cold pizza, melted ice cream).  
                - The item is **missing** (e.g., "I ordered three items, but only two arrived").  
                - The order **never arrived** (e.g., "I waited for an hour, but no delivery").  
                - The order was **significantly delayed** (e.g., "It was supposed to arrive in 30 minutes, but it's been two hours").  
                - The user **explicitly asks for a refund** (e.g., "I want my money back").  

                #### **Non-Refundable Issues** (Respond with 'non_refundable')  
                A complaint is **non-refundable** if it involves:  
                - **Asking about ETA** (e.g., "Where is my order?", "How much time left?").  
                - **Rude behavior from the delivery agent** (e.g., "The driver was impolite", "The agent was not professional").  
                - **Minor service complaints** that do not impact the order quality (e.g., "The delivery person was late but still delivered my food in good condition").  

                ### **Response Format**  
                Respond with only one word: `refundable` or `non_refundable`.  
                """


        # Uncomment to use actual classification
        classification_raw = self.classifier_llm.invoke(prompt).content
        if "refundable" in classification_raw.lower():
            state["classification"] = "refundable"
        else:
            state["classification"] = "non_refundable"
        
        # For testing/simulation purposes
        # state["classification"] = "refundable"
        print(f"LLM classification result => {state['classification']}")
        return state

    def problem_verify(self, state: SomeState) -> dict:
        """
        Verify user's problem with image proof.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with verification result
        """
        print("\n[Node: problem_verify]")

        prdct_name = input("Please enter your item name: ")
        state["refund_prdct"] = prdct_name
        problem_image_path = input("Please enter your image proof: ").strip()
        problem_image_path = problem_image_path.replace("\\", "/")  
        state["image_problem_path"] = problem_image_path
        bill_image_path = input("Please enter your bill proof: ")
        bill_image_path = bill_image_path.replace("\\", "/")
        state["image_bill_path"] = bill_image_path
        print("Thanks Please wait while we process your request")

        # Process the image with vision model
        prompt = f"<|image_1|>\n does this image match with the customer complaint : {state['user_first_message']}, Reply with only YES or NO"
        print(prompt)
        try:
            url = state["image_problem_path"]
            image = Image.open(url)
            image.show()

            inputs = self.ov_model.preprocess_inputs(
                text=prompt, 
                image=image, 
                processor=self.processor
            )

            generation_args = {
                "max_new_tokens": 50,
                "temperature": 0.0,
                "do_sample": False,
                "streamer": TextStreamer(self.processor.tokenizer, skip_prompt=True, skip_special_tokens=True)
            }

            generate_ids = self.ov_model.generate(
                **inputs,
                eos_token_id=self.processor.tokenizer.eos_token_id,
                **generation_args
            )

            generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]
            response = self.processor.batch_decode(
                generate_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False
            )[0]
            
            print(f"LLM verification result => {response}")
            state["verified"] = response.lower() != "no"
        except Exception as e:
            print(f"Error in problem verification: {e}")
            state["verified"] = False
            
        print(f"Verification result => {state['verified']}")
        return state

    def agent(self, state: SomeState) -> dict:
        """
        Conversational agent for handling user interactions.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with conversation history
        """
        print("\n[Node: Agent]")
        user_message = state.get("user_message", "")

        # Process the current message if there is one
        if user_message:
            response = self.agent_conversation_chain.run(user_message)
            print(f"Agent says: {response}")
            state["notes"] += f"\n[Agent conversation] User: {user_message}\nAgent: {response}"

            # Get a new message from the user for the next turn
            new_message = input("Your response: ")
            state["user_message"] = new_message
        else:
            print("No user message provided this turn.")
            # Still try to get input even if no message was initially provided
            new_message = input("Please provide your message: ")
            state["user_message"] = new_message

        return state

    def eta_tool(self, state: SomeState) -> dict:
        """
        Provide estimated delivery time information.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with ETA information
        """
        print("\n[Node: ETA_tool]")
        print("Simulated: The order will arrive in ~30 minutes.")
        state["notes"] += "\n[ETA_tool] Provided an ETA of ~30 minutes (simulated)."
        return state

    def check_resolution(self, state: SomeState) -> dict:
        """
        Check if the user's issue has been resolved.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with resolution status
        """
        print("\n[Node: check_resolution]")
        user_input = input("Has your issue been resolved? (yes/no): ").strip().lower()
        state["resolved"] = user_input.startswith('y')
        print(f"Issue resolved? => {state['resolved']}")
        return state

    def human_in_the_loop(self, state: SomeState) -> dict:
        """
        Escalate to human support agent.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with escalation notes
        """
        print("\n[Node: human_in_the_loop]")
        print("Simulated: Escalating to a human support agent. (End of automation)")
        state["notes"] += "\n[human_in_the_loop] Issue escalated to a human agent."
        return state

    def service_complaint(self, state: SomeState) -> dict:
        """
        Handle service-related complaints.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with complaint notes
        """
        print("\n[Node: Service_complaint]")
        print("Simulated: Logging your complaint about the delivery service.")
        state["notes"] += "\n[Service_complaint] Complaint logged (simulated)."
        return state
        
    def bill_amount_verification(self, state: SomeState) -> dict:
        """
        Verify bill amount from uploaded image.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with verified refund amount
        """
        print("\n[Node: Bill_Amount_verification]")
        
        try:
            prompt = f"<|image_1|>\n what is the price of the following item {state['refund_prdct']} reply with only the numeric value no currency"

            url = state["image_bill_path"]
            image = Image.open(url)
            image.show()
            
            inputs = self.ov_model.preprocess_inputs(
                text=prompt, 
                image=image, 
                processor=self.processor
            )

            generation_args = {
                "max_new_tokens": 50,
                "temperature": 0.0,
                "do_sample": False,
                "streamer": TextStreamer(self.processor.tokenizer, skip_prompt=True, skip_special_tokens=True)
            }

            generate_ids = self.ov_model.generate(
                **inputs,
                eos_token_id=self.processor.tokenizer.eos_token_id,
                **generation_args
            )

            generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]
            response = self.processor.batch_decode(
                generate_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False
            )[0]

            print(f"LLM bill result => {response}")
            try:
                state["refund_amount"] = int(response)
            except ValueError:
                print("Could not parse amount as integer, defaulting to 0")
                state["refund_amount"] = 0
                
        except Exception as e:
            print(f"Error in bill verification: {e}")
            state["refund_amount"] = 0
            
        return state

    def refund_tool(self, state: SomeState) -> dict:
        """
        Process refund for the customer.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with refund information
        """
        print("\n[Node: Refund_Tool]")
        print(f"Amount refunded: {state['refund_amount']}")
        state["notes"] += f"\n[Refund_Tool] Processed refund of {state['refund_amount']} for {state['refund_prdct']}"
        return state