
```python



import anthropic


def create_workout_tracker_guide():
    
    
    client = anthropic.Anthropic()
    
    prompt = 

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    return message.content[0].text


def display_guide(guide_text):
    
    print("=" * 80)
    print("WORKOUT TRACKING NOTEBOOK - BEGINNER'S GUIDE FOR EXCEL")
    print("=" * 80)
    print("\n")
    print(guide_text)
    print("\n")
    print("=" * 80)


def main():
    
    print("Generating personalized guide for Harold...")
    print("(This may take a moment as Claude creates the instructions)")
    print()
    
    guide = create_workout_tracker_guide()
    display_guide(guide)
    
    print("\nGuide generation complete!")
    print("Save this information and follow the steps to create your Excel workout tracker.")


if __name__ == "__main__":
    main()
```