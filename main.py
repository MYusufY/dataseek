import webview
import json
import os
from deepseekr import DeepSeek
import threading

class DataSeekAPI:
    def __init__(self):
        self.deepseek = None
        self.window = None
        self.stop_flag = False
    
    def set_window(self, window):
        self.window = window
    
    def update_status(self, message):
        if self.window:
            self.window.evaluate_js(f'updateStatus("{message}")')
        print(message)
    
    def start_datasetify(self, config):
        self.stop_flag = False
        threading.Thread(target=self._process_dataseek, args=(config,)).start()
    
    def stop_process(self):
        self.stop_flag = True
        self.update_status("Stopping process...")
        if self.window:
            self.window.evaluate_js('resetButtons()')
    
    def _process_dataseek(self, config):
        try:
            self.update_status("Initializing DeepSeek...")
            self.deepseek = DeepSeek(chrome_path="/Applications/Chrome.app/Contents/MacOS/Google Chrome")
            
            if self.stop_flag:
                return
            
            self.update_status("Sending system prompt to DeepSeek...")
            system_response = self.deepseek.send_prompt(config['systemPrompt'])
            print(f"System Response: {system_response}")
            
            if self.stop_flag:
                return
            
            training_data = []
            if config['trainingData'].strip():
                self.update_status("Creating dataseek.json...")
                with open('dataseek.json', 'w', encoding='utf-8') as f:
                    f.write(config['trainingData'])
                
                if self.stop_flag:
                    return
                
                self.update_status("Loading training data...")
                try:
                    with open('dataseek.json', 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        if content.startswith('[') and content.endswith(']'):
                            training_data = json.loads(content)
                        else:
                            lines = content.strip().split('\n')
                            for line in lines:
                                if line.strip():
                                    training_data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    self.update_status(f"JSON parsing error: {e}")
                    return
                
                if self.stop_flag:
                    return
                
                self.update_status("Sending last 30 examples to DeepSeek...")
                last_30 = training_data[-30:] if len(training_data) > 30 else training_data
                examples_text = "\n".join([json.dumps(item, ensure_ascii=False) for item in last_30])
                self.deepseek.send_prompt(examples_text)
            else:
                self.update_status("No training data provided, starting with empty dataset...")
            
            if config['mode'] == 'repeat':
                iterations = config['count']
            elif config['mode'] == 'example':
                iterations = config['count'] // 30
            else:
                iterations = float('inf')
            
            if config['mode'] == 'until_stop':
                self.update_status("Running until stopped...")
            else:
                self.update_status(f"Starting {iterations} iterations...")
            
            i = 0
            while (i < iterations or config['mode'] == 'until_stop') and not self.stop_flag:
                i += 1
                if config['mode'] == 'until_stop':
                    self.update_status(f"Iteration {i}")
                else:
                    self.update_status(f"Iteration {i}/{iterations}")
                
                response = self.deepseek.send_prompt("OK")
                print(f"Response {i}: {response}")
                
                try:
                    response_lines = response.strip().split('\n')
                    new_data = []
                    for line in response_lines:
                        line = line.strip()
                        if line and (line.startswith('{') and line.endswith('}')):
                            try:
                                new_item = json.loads(line)
                                new_data.append(new_item)
                            except json.JSONDecodeError:
                                continue
                    
                    if new_data:
                        training_data.extend(new_data)
                        
                        output_file = 'dataseek.json' if config['trainingData'].strip() else 'dataseek_generated.json'
                        with open(output_file, 'w', encoding='utf-8') as f:
                            for item in training_data:
                                f.write(json.dumps(item, ensure_ascii=False) + '\n')
                        
                        self.update_status(f"Added {len(new_data)} new examples. Total: {len(training_data)}")
                    else:
                        self.update_status(f"No valid JSON found in response {i}")
                        
                except Exception as e:
                    self.update_status(f"Error processing response {i}: {e}")
                    continue
            
            if self.stop_flag:
                self.update_status("Process stopped by user")
            else:
                self.update_status(f"Process completed! Generated {len(training_data)} total examples")
            
            if self.window:
                self.window.evaluate_js('resetButtons()')
            
        except Exception as e:
            self.update_status(f"Error: {e}")
            if self.window:
                self.window.evaluate_js('resetButtons()')
        finally:
            if self.deepseek:
                try:
                    self.deepseek.close()
                except:
                    pass

def main():
    api = DataSeekAPI()
    
    with open('src/gui.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    window = webview.create_window(
        'DataSeek',
        html=html_content,
        js_api=api,
        width=900,
        height=700,
        resizable=True
    )
    
    api.set_window(window)
    webview.start(debug=False)

if __name__ == '__main__':
    main()